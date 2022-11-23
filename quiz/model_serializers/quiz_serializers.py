from rest_framework import serializers

from quiz.model_serializers.question_serializers import QuestionSecretSerializer, QuestionSerializer
from quiz.models import Quiz, Question


class QuizReadSerializer(serializers.ModelSerializer):
    questions = QuestionSecretSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions']


class QuizWriteSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions']

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        validated_data['owner'] = self.context['request'].user
        quiz = super(QuizWriteSerializer, self).create(validated_data)
        for question_data in questions:
            question = Question(**question_data, quiz=quiz)
            question.save()
        return quiz

    def update(self, instance, validated_data):
        questions = validated_data.pop('questions')
        instance.questions.all().delete()
        for question_data in questions:
            question = Question(**question_data, quiz=instance)
            question.save()
        return super(QuizWriteSerializer, self).update(instance, validated_data)
