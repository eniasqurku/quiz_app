from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from quiz.models import Question, Quiz, ParticipantAnswer
from quiz.serializers.option_serializer import OptionSerializer


class QuestionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "title"]


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "title", "options"]

    def create(self, validated_data):
        quiz_id = self.context["view"].kwargs["quiz_id"]
        quiz = get_object_or_404(Quiz, pk=quiz_id)

        if quiz.owner != self.context["request"].user:
            raise ValidationError(
                "You do not have permission to create questions for this quiz",
                code=status.HTTP_403_FORBIDDEN,
            )
        validated_data["quiz"] = quiz

        return super().create(validated_data)


class QuestionResultSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ["id", "title", "options", "answer"]

    def get_answer(self, instance: Question):
        participant = self.context["participant"]
        answer = ParticipantAnswer.objects.filter(
            participant=participant, question=instance
        ).first()

        return answer.answer_id if answer else None
