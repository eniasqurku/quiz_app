from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from quiz.models import ParticipantAnswer
from quiz.serializers.question_serializers import (
    QuestionSerializer,
)


class AnswerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantAnswer
        fields = ["id", "question", "answer"]

    def create(self, validated_data):
        validated_data["participant"] = self.context["request"].user
        answer = super().create(validated_data)
        self._check_can_answer(answer)

        return answer

    def update(self, instance, validated_data):
        answer = super().update(instance, validated_data)
        self._check_can_answer(answer)

        return answer

    @staticmethod
    def _check_can_answer(answer) -> None:
        if not answer.can_answer():
            raise ValidationError(
                "Question does not belong to participant quizzes "
                "or the option chose does not belong the question",
                code=status.HTTP_400_BAD_REQUEST,
            )


class AnswerReadSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = ParticipantAnswer
        fields = ["id", "question", "answer"]
