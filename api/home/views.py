from . serialziers import *
from . models import *
from api.core.mixin import DotsModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class PrincipleViewSet(DotsModelViewSet):
    queryset = Principle.objects.all().order_by("order")
    serializer_class = PrincipleSerializer
    serializer_create_class = PrincipleSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["GET"], url_path="categories/questions")
    def principle_related_categories_question(self, request, *args, **kwargs):
        principle = self.get_object()
        questions = Question.objects.filter(principle=principle)\
            .select_related('category', 'pest_type', 'principle')\
            .order_by("order")
        principle_data = PrincipleSerializer(principle).data

        categories = {}
        for question in questions:
            category = question.category
            pest_type = question.pest_type
            
            if category.id not in categories:
                categories[category.id] = {'category': CategoriesSerializer(category).data, 'pest_types': {}}
            
            pest_type_key = pest_type.id if pest_type else 'general'
            if pest_type_key not in categories[category.id]['pest_types']:
                categories[category.id]['pest_types'][pest_type_key] = { 'pest_type': PestTypeSerializer(pest_type).data if pest_type else None, 'questions': []}

            answer = question.answer_set.filter(created_by=request.user).first()
            categories[category.id]['pest_types'][pest_type_key]['questions'].append(
                    {
                        "question": ShortQuestionSerializer(question).data,
                        "answer": AnswerSerializer(answer).data if answer else None
                    }
                )
        
        response_data = [
            {'category': category_data['category'], 'pest_types': list(category_data['pest_types'].values())}
            for category_data in categories.values()
        ]
        
        return Response({'principle': principle_data,'categories': response_data}, status=200)

    @action(detail=False, methods=["GET"], url_path="status")
    def principles_status(self, request, *args, **kwargs):
        principles = self.get_queryset()
        status_list = []

        for principle in principles:
            questions = Question.objects.filter(principle=principle)\
                .select_related('category')\
                .prefetch_related('answer_set')
            
            answered_categories = set()
            all_categories = set()
            
            for question in questions:
                all_categories.add(question.category.id)
                if question.answer_set.filter(created_by=request.user).exists():
                    answered_categories.add(question.category.id)
            
            # Determine if principle is completed
            is_completed = len(answered_categories) == len(all_categories) and len(all_categories) > 0
            
            status_list.append({
                'id': principle.id,
                'name': principle.name,
                'status': 'completed' if is_completed else 'pending',
                'completed_categories': len(answered_categories),
                'total_categories': len(all_categories),
                'progress': f"{len(answered_categories)}/{len(all_categories)}" if all_categories else "0/0"
            })
        
        return Response(status_list)


class CategoriesViewSet(DotsModelViewSet):
    queryset = Category.objects.all().order_by("order")
    serializer_class = CategoriesSerializer
    serializer_create_class = CategoriesSerializer


class PestTypeViewSet(DotsModelViewSet):
    queryset = PestType.objects.all()
    serializer_class = PestTypeSerializer
    serializer_create_class = PestTypeSerializer


class QuestionGroupViewSet(DotsModelViewSet):
    queryset = QuestionGroup.objects.all().order_by("order")
    serializer_class = QuestionGroupSerializer
    serializer_create_class = QuestionGroupSerializer


class QuestionViewSet(DotsModelViewSet):
    queryset = Question.objects.all().order_by("order")
    serializer_class = QuestionSerializer
    serializer_create_class = QuestionSerializer


class AnswerViewSet(DotsModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = ShortAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'by_question', 'upload_images']:
            return AnswerSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.validated_data["created_by"] = self.request.user
        return super().perform_create(serializer)

    @action(detail=True, methods=['post'], url_path='upload-images')
    def upload_images(self, request, pk=None):
        answer = self.get_object()
        images = request.FILES.getlist('images')
        for image in images:
            photo = Photo.objects.create(image=image, uploaded_by=request.user)
            answer.images.add(photo)
        answer.refresh_from_db()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='by-question/(?P<question_id>\d+)')
    def by_question(self, request, question_id=None):
        answers = self.get_queryset().filter(question_id=question_id)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(answers, many=True)
        return Response(serializer.data)
    

class PhotosViewSet(DotsModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]




