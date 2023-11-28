from rest_framework import serializers

from agent.serializers.agent_serializers import UserReadSerializer
from quiz.models import QuizAttempt
from quiz.serializers.quiz_serializers import QuizReducedSerializer


class QuizAttemptWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ["id", "participant", "quiz"]
        read_only_fields = ["participant"]

    def create(self, validated_data):
        validated_data["participant"] = self.context["request"].user
        return super().create(validated_data)


class QuizAttemptReadSerializer(serializers.ModelSerializer):
    quiz = QuizReducedSerializer()
    participant = UserReadSerializer()

    class Meta:
        model = QuizAttempt
        fields = ["id", "participant", "quiz"]
