from rest_framework import serializers

from quiz.models import Quiz, QuizAttempt
from quiz.serializers.question_serializers import (
    QuestionSerializer,
    QuestionResultSerializer,
)


class QuizReducedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "title"]


class QuizReadSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "questions"]


class QuizWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "title"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super(QuizWriteSerializer, self).create(validated_data)


class QuizResultSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    questions = QuestionResultSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "progress", "score", "questions"]

    def get_progress(self, obj):
        participant = self.context["participant"]
        quiz_attempt = QuizAttempt.objects.get(participant=participant, quiz=obj)

        return quiz_attempt.progress

    def get_score(self, obj):
        participant = self.context["participant"]
        quiz_attempt = QuizAttempt.objects.get(participant=participant, quiz=obj)

        return f"{quiz_attempt.score} %"
