from .serializers import *
from . models import *
from api.core.mixin import DotsModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import OuterRef, Exists, Case, When, Value, BooleanField, Subquery, Prefetch
from django.db.models.functions import Coalesce

class PrincipleViewSet(DotsModelViewSet):
    queryset = Principle.objects.all().order_by("order")
    serializer_class = PrincipleSerializer
    serializer_create_class = PrincipleSerializer
    permission_classes = [IsAuthenticated]

    def _get_customer(self, customer_id):
        try:
            return Customer.objects.get(id=customer_id)
        except (Customer.DoesNotExist, ValueError, TypeError):
            return None

    @action(detail=True, methods=["GET"], url_path="categories")
    def principle_categories(self, request, *args, **kwargs):
        principle = self.get_object()
        customer_id = self.request.GET.get("customer_id")
        customer = self._get_customer(customer_id) if customer_id else None

        def annotated_category_qs():
            qs = Category.objects.order_by('order')
            if customer:
                customer_applicable_qs = CategoryApplicability.objects.filter(customer=customer, category=OuterRef('pk')).values('applicable')[:1]
                qs = qs.annotate(
                    is_answered=Exists(SelectedOption.objects.filter(customer=customer, category=OuterRef('pk'), selected=True)),
                    applicable=Coalesce(Subquery(customer_applicable_qs), Value(True), output_field=BooleanField())
                )
                options_qs = Option.objects.annotate(
                    is_selected=Case(
                        When(Exists(SelectedOption.objects.filter(customer=customer, option=OuterRef('pk'), selected=True)), then=True),
                        default=False,
                        output_field=BooleanField()
                    )
                )
                qs = qs.prefetch_related(Prefetch('options', queryset=options_qs))
            else:
                qs = qs.annotate(applicable=Value(True)).prefetch_related('options')
            return qs

        if customer:
            customer_applicable_qs = CategoryApplicability.objects.filter(customer=customer, category=OuterRef('pk')).values('applicable')[:1]
            options_qs = Option.objects.annotate(
                is_selected=Case(
                    When(Exists(SelectedOption.objects.filter(customer=customer, option=OuterRef('pk'), selected=True)), then=True),
                    default=False,
                    output_field=BooleanField()
                )
            )

            categories = Category.objects.filter(principle=principle, parent__isnull=True) \
                .order_by('order') \
                .annotate(
                    is_answered=Exists(SelectedOption.objects.filter(customer=customer, category=OuterRef('pk'), selected=True)),
                    applicable=Coalesce(Subquery(customer_applicable_qs), Value(True), output_field=BooleanField())
                ) \
                .prefetch_related(
                    Prefetch('options', queryset=options_qs),
                    Prefetch('subcategories',queryset=annotated_category_qs().prefetch_related(
                        Prefetch('subcategories', queryset=annotated_category_qs())
                        )
                    )
                )
        else:
            categories = Category.objects.filter(principle=principle, parent__isnull=True) \
                .order_by('order') \
                .annotate(applicable=Value(True)) \
                .prefetch_related(
                    Prefetch('options'),
                    Prefetch('subcategories', queryset=annotated_category_qs().prefetch_related(
                        Prefetch('subcategories', queryset=annotated_category_qs())
                    ))
                )

        response_data = {'principle': principle, 'categories': categories}
        serializer = PrincipleCategoriesSerializer(response_data, context={'customer': customer})
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=["GET"], url_path="status")
    def principles_status(self, request, *args, **kwargs):
        principles = self.get_queryset()
        customer_id = request.GET.get("customer_id")        
        status_data = []
        customer = self._get_customer(customer_id) if customer_id else None

        for principle in principles:
            main_categories = Category.objects.filter(principle=principle, parent__isnull=True)
            total_main_categories = main_categories.count()
            
            answered_count = 0
            if customer:
                for main_category in main_categories:
                    has_subcategories = Category.objects.filter(parent=main_category).exists()
                    
                    if has_subcategories:
                        subcategory_answered = SelectedOption.objects.filter(customer=customer, category__parent=main_category, selected=True).exists()
                        subcategory_applicable = CategoryApplicability.objects.filter(customer=customer, category__parent=main_category, applicable=False).exists()
                        if subcategory_applicable or subcategory_answered:
                            answered_count += 1
                    else:
                        category_answered = SelectedOption.objects.filter(customer=customer, category=main_category, selected=True).exists()
                        category_applicable = CategoryApplicability.objects.filter(customer=customer, category=main_category, applicable=False).exists()
                        if category_answered or category_applicable:
                            answered_count += 1                    
            
            is_completed = answered_count == total_main_categories and total_main_categories > 0
            status_data.append({
                'id': principle.id,
                'name': principle.name,
                'status': 'completed' if is_completed else 'pending',
                'completed_categories': answered_count,
                'total_categories': total_main_categories,
                'progress': f"{answered_count}/{total_main_categories}" if total_main_categories else "0/0"
            })
        
        serializer = PrincipleStatusSerializer(status_data, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CategoryViewSet(DotsModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['POST'], url_path='feedback')
    def submit_answer(self, request, pk=None):
        input_serializer = AnswerSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        category = self.get_object()
        validated_data = input_serializer.validated_data
        customer = validated_data['customer_id']
        note = validated_data['note']
        with transaction.atomic():
            feedback, created = Feedback.objects.get_or_create(customer=customer, category=category, defaults={'note': note})
            if not created:
                feedback.note = note
                feedback.save()
        return Response(status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['POST'], url_path='selection')
    def option_section(self, request, *args, **kwargs):
        selection_serializer = SelectionSerializer(data=request.data)
        selection_serializer.is_valid(raise_exception=True)
        category = self.get_object()
        validated_data = selection_serializer.validated_data
        customer = validated_data['customer_id']
        selected_option_ids = validated_data['selected_options']
        with transaction.atomic():
            SelectedOption.objects.filter(customer=customer, category=category).delete()
            for option_id in selected_option_ids:
                try:
                    option = Option.objects.get(id=option_id, category=category)
                    SelectedOption.objects.create(customer=customer, category=category, option=option, selected=True)
                except Option.DoesNotExist:
                    return Response({"error": f"Option {option_id} not found for this category"}, status=status.HTTP_400_BAD_REQUEST)
            CategoryApplicability.objects.update_or_create(customer=customer, category=category, defaults={"applicable": True})
        return Response(status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['POST'], url_path='applicable')
    def applicable(self, request, *args, **kwargs):
        applicable_serializer = ApplicableSerializer(data=request.data)
        applicable_serializer.is_valid(raise_exception=True)
        category = self.get_object()
        validated_data = applicable_serializer.validated_data
        customer = validated_data['customer_id']
        
        with transaction.atomic():
            SelectedOption.objects.filter(customer=customer, category=category).delete()
            Feedback.objects.filter(customer=customer, category=category).delete()
            CategoryApplicability.objects.update_or_create(customer=customer, category=category, defaults={"applicable": False})
            
            if category.parent:
                self._check_and_update_parent_applicability(customer, category.parent)
            if category.subcategories.exists():
                # This is a parent category, mark all subcategories as not applicable too
                subcategories = category.subcategories.all()
                for subcategory in subcategories:
                    # Delete selected options and feedback for subcategories
                    SelectedOption.objects.filter(customer=customer, category=subcategory).delete()
                    Feedback.objects.filter(customer=customer, category=subcategory).delete()
                    CategoryApplicability.objects.update_or_create(customer=customer, category=subcategory, defaults={"applicable": False})
    
        return Response(status=status.HTTP_200_OK)

    def _check_and_update_parent_applicability(self, customer, parent_category):
        subcategories = parent_category.subcategories.all()
        if not subcategories.exists(): return
        applicable_subcategories = CategoryApplicability.objects.filter(customer=customer, category__in=subcategories, applicable=True).exists()
        if not applicable_subcategories:
            Feedback.objects.filter(customer=customer, category=parent_category).delete()
            if parent_category.parent:
                self._check_and_update_parent_applicability(customer, parent_category.parent)


    @action(detail=True, methods=['POST'], url_path='upload-images')
    def upload_images(self, request, pk=None):
        category = self.get_object()
        customer_id = request.data.get('customer_id')
        images = request.FILES.getlist('images')
        
        if not customer_id:
            return Response({"error": "customer_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not images:
            return Response({"error": "images are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        feedback, created = Feedback.objects.get_or_create(customer=customer, category=category)
        uploaded_images = []
        for image in images:
            photo = Photo.objects.create(image=image)
            feedback.images.add(photo)
            uploaded_images.append(photo)
        response_data = {"message": f"{len(uploaded_images)} images uploaded successfully", "images": uploaded_images, "feedback": FeedbackSerializer(feedback).data}
        serializer = UploadImagesResponseSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PhotoViewSet(DotsModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]


class FeedbackViewSet(DotsModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]


class CustomerViewSet(DotsModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = ReturnCustomerSerializer
    serializer_create_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(created_by=self.request.user)
        if self.action in ["list"]:
            queryset = queryset.filter(audit_completed=True)
        return queryset

    def _get_customer(self, customer_id):
        try:
            return Customer.objects.get(id=customer_id)
        except (Customer.DoesNotExist, ValueError, TypeError):
            return None
        
    def get_or_create_customer(self, customer_id=None):
        if customer_id:
            customer = self._get_customer(customer_id)
            if customer:
                return customer
        current_user = self.request.user
        return Customer.create_default_customer(current_user)
    
    def create(self, request, *args, **kwargs):
        if not request.data:
            customer = self.get_or_create_customer()
            serializer = self.get_serializer(customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['created_by'] = request.user
        
        if 'address' not in serializer.validated_data:
            serializer.validated_data['address'] = None
        if 'city' not in serializer.validated_data:
            serializer.validated_data['city'] = None
        if 'state' not in serializer.validated_data:
            serializer.validated_data['state'] = None
        if 'zip' not in serializer.validated_data:
            serializer.validated_data['zip'] = None
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)