from rest_framework import serializers

from quiz.models import TakenQuiz


class TakenQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakenQuiz
        fields = ['id', 'quiz']

    def create(self, validated_data):
        validated_data['participant'] = self.context['request'].user
        quiz = super(TakenQuizSerializer, self).create(validated_data)
        return quiz
