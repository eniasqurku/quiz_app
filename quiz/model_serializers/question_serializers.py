from rest_framework import serializers

from quiz.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_answer', 'quiz']


class QuestionSecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'option_1', 'option_2', 'option_3', 'option_4']
