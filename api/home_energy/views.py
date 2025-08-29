from .models import *
from .serializers import *
from django.db.models import Exists, OuterRef, Value, Case, When, BooleanField, Subquery, Prefetch
from api.core.mixin import DotsModelViewSet
from rest_framework.permissions import AllowAny
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
                    is_answered = bool(answer_obj.text or answer_obj.numeric_answer or answer_obj.images.exists())
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
    
    
class QuestionsViewSet(DotsModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]


class FeedbackeViewSet(DotsModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


