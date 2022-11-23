from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from quiz.model_serializers.question_serializers import QuestionSerializer, QuestionSecretSerializer
from quiz.models import ParticipantAnswer


class AnswerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantAnswer
        fields = ['id', 'question', 'answer']

    def create(self, validated_data):
        answer = ParticipantAnswer(**validated_data, participant=self.context['request'].user)
        if not answer.can_answer():
            raise ValidationError('Question does not belong to participant quizzes')
        answer.save()

        return answer


class AnswerReadSerializer(serializers.ModelSerializer):
    quiz = SerializerMethodField()

    class Meta:
        model = ParticipantAnswer
        fields = ['id', 'question', 'answer', 'quiz', 'participant']

    def get_quiz(self, obj):
        return obj.question.quiz_id


class AnswerWithQuestionSerializer(serializers.ModelSerializer):
    quiz = SerializerMethodField()
    is_correct = SerializerMethodField()
    question = QuestionSerializer()

    class Meta:
        model = ParticipantAnswer
        fields = ['id', 'question', 'answer', 'quiz', 'is_correct']

    def get_quiz(self, obj):
        return obj.question.quiz_id

    def get_correct_answer(self, obj):
        return obj.question.correct_answer

    def get_is_correct(self, obj):
        return obj.is_correct()


class AnswerWithQuestionSecretSerializer(serializers.ModelSerializer):
    quiz = SerializerMethodField()
    question = QuestionSecretSerializer()

    class Meta:
        model = ParticipantAnswer
        fields = ['id', 'question', 'quiz', 'answer']

    def get_quiz(self, obj):
        return obj.question.quiz_id
