from .models import *
from .serializers import *
from django.db.models import Exists, OuterRef, Value, Case, When, BooleanField, Subquery, Prefetch
from django.db import transaction
from api.core.mixin import DotsModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response


class StepViewSet(DotsModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = [AllowAny]

    def _get_customer(self, customer_id):
        try:
            return Customer.objects.get(id=customer_id)
        except (Customer.DoesNotExist, ValueError, TypeError):
            return None

    @action(detail=True, methods=["GET"], url_path="questions")
    def questions(self, request, *args, **kwargs):
        step = self.get_object()
        customer_id = self.request.GET.get("customer_id")
        customer = self._get_customer(customer_id) if customer_id else None

        options_qs = Option.objects.all()
        if customer:
            options_qs = options_qs.annotate(
                is_selected=Case(
                    When(Exists(SelectedOptions.objects.filter(customer=customer, option=OuterRef("pk"))), then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
        else:
            options_qs = options_qs.annotate(is_selected=Value(False, output_field=BooleanField()))
        question_prefetches = [Prefetch("options", queryset=options_qs)]
        if customer:
            question_prefetches.append(Prefetch("question_answers", queryset=Answer.objects.filter(customer=customer), to_attr="customer_answers"))
        questions_qs = Question.objects.all().order_by("id").prefetch_related(*question_prefetches)
        groups_qs = (QuestionGroup.objects.filter(step=step).prefetch_related(Prefetch("question", queryset=questions_qs, to_attr="prefetched_questions")))
        if customer:
            groups_qs = groups_qs.prefetch_related(Prefetch("responses", queryset=Feedback.objects.filter(customer=customer).prefetch_related("images"), to_attr="customer_feedback"))

        data_groups = []
        for grp in groups_qs:
            feedback_obj = None
            if hasattr(grp, "customer_feedback") and grp.customer_feedback:
                feedback_obj = grp.customer_feedback[0]

            serialized_questions = []
            for q in getattr(grp, "prefetched_questions", []):
                answer_obj = None
                if hasattr(q, "customer_answers") and q.customer_answers:
                    answer_obj = q.customer_answers[0]

                is_answered = False
                if answer_obj:
                    is_answered = bool(answer_obj.text)
                any_selected = any(getattr(opt, "is_selected", False) for opt in q.options.all())
                is_answered = is_answered or any_selected

                serialized = {
                    **QuestionWithOptionsSerializer(q).data, 
                    "answer": (AnswerSerializer(answer_obj).data if answer_obj else None),
                    "is_answered": is_answered,
                }
                serialized_questions.append(serialized)

            data_groups.append(
                {
                    "id": grp.id,
                    "questions": serialized_questions,
                    "feedback": (FeedbackSerializer(feedback_obj).data if feedback_obj else None),
                }
            )
        response_data = {"step": StepSerializer(step).data, "groups": data_groups}
        return Response(response_data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["GET"], url_path="status")
    def step_status(self, request, *args, **kwargs):
        step = self.get_object()
        customer_id = self.request.GET.get("customer_id")
        customer = self._get_customer(customer_id) if customer_id else None
        groups_qs = QuestionGroup.objects.filter(step=step)
        total_groups = groups_qs.count()
        completed_groups = 0

        if customer:
            for grp in groups_qs:
                is_completed = False
                has_answer = Answer.objects.filter(customer=customer, question__in=grp.question.all(), text__isnull=False).exists()
                has_selected_option = SelectedOptions.objects.filter(customer=customer, question__in=grp.question.all()).exists()
                has_feedback = Feedback.objects.filter(customer=customer, question_group=grp).exists()

                if has_answer or has_selected_option or has_feedback:
                    is_completed = True

                if is_completed:
                    completed_groups += 1

        is_step_completed = total_groups > 0 and completed_groups == total_groups

        status_data = {
            "id": step.id,
            "title": step.title,
            "status": "completed" if is_step_completed else "pending",
            "completed_groups": completed_groups,
            "total_groups": total_groups,
            "progress": f"{completed_groups}/{total_groups}" if total_groups else "0/0",
        }

        return Response(status_data, status=status.HTTP_200_OK)
    

class QuestionGroupViewSet(DotsModelViewSet):
    queryset = QuestionGroup.objects.all()
    serializer_class = QuestionGroupSerialzier
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["customer_id"] = self.request.GET.get("customer_id")
        return context
    
    @action(detail=True, methods=['POST'], url_path='feedback')
    def feedback(self, request, pk=None):
        input_serializer = HomeEnergyAnswerSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        question_group = self.get_object()
        validated_data = input_serializer.validated_data
        customer = validated_data["customer_id"]
        text = validated_data['text']
        with transaction.atomic():
            feedback, created = Feedback.objects.get_or_create(customer=customer, question_group=question_group, defaults={'text':text})
            if not created:
                feedback.text = text
            feedback.save()
        serializer = self.get_serializer(question_group, context={"customer_id": customer.id})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['POST'], url_path='upload-images')
    def upload_images(self, request, pk=None):
        question_group = self.get_object()
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
        
        feedback, created = Feedback.objects.get_or_create(customer=customer, question_group=question_group)
        uploaded_images = []
        for image in images:
            photo = Photo.objects.create(image=image)
            feedback.images.add(photo)
            uploaded_images.append(photo)
        response_data = {"message": f"{len(uploaded_images)} images uploaded successfully", "feedback": FeedbackSerializer(feedback).data}
        serializer = UploadImagesResponseSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class QuestionsViewSet(DotsModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['POST'], url_path='selection')
    def selection(self, request, *args, **kwargs):
        selection_serializer = SelectionSerializer(data=request.data)
        selection_serializer.is_valid(raise_exception=True)
        question = self.get_object()
        validated_data = selection_serializer.validated_data
        customer = validated_data['customer_id']
        selected_option_ids = validated_data['selected_options']
        with transaction.atomic(): 
            SelectedOptions.objects.filter(customer=customer, question=question).delete()
            for option_id in selected_option_ids:
                try:
                    option = Option.objects.get(id=option_id, question=question)
                    SelectedOptions.objects.create(customer=customer, question=question, option=option)
                except Option.DoesNotExist:
                    return Response({"error": f"Option {option_id} not found for this category"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'], url_path='answer')
    def answer(self, request, *args, **kwargs):
        selection_serializer = QuestionAnswerSerializer(data=request.data)
        selection_serializer.is_valid(raise_exception=True)
        question = self.get_object()
        validated_data = selection_serializer.validated_data
        customer = validated_data['customer_id']
        text = validated_data['text']
        with transaction.atomic():
            answer, created = Answer.objects.get_or_create(customer=customer, question=question,  defaults={'text': text})
            if not created:
                answer.text = text
                answer.save()
        return Response(status=status.HTTP_201_CREATED)


class QuestionGroupFeedbackViewSet(DotsModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]


class AnswerViewSet(DotsModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [AllowAny]