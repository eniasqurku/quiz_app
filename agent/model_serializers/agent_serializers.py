from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from agent.models import User
from quiz.model_serializers.answer_serializers import AnswerWithQuestionSerializer, AnswerWithQuestionSecretSerializer
from quiz.models import Quiz, ParticipantAnswer, TakenQuiz


class UserReadSerializer(ModelSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'groups', 'full_name', 'is_active']

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserQuizzesSerializer(ModelSerializer):
    answers = SerializerMethodField()
    progress = SerializerMethodField()
    score = SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'progress', 'score', 'answers']

    def get_answers(self, obj):
        participant = User.objects.get(id=self.context['view'].kwargs['pk'])
        answers = ParticipantAnswer.objects.filter(participant=participant, question__quiz=obj)

        return AnswerWithQuestionSerializer(answers, many=True).data

    def get_progress(self, obj):
        participant = User.objects.get(id=self.context['view'].kwargs['pk'])
        taken_quiz = TakenQuiz.objects.get(participant=participant, quiz=obj)

        return taken_quiz.progress()

    def get_score(self, obj):
        participant = User.objects.get(id=self.context['view'].kwargs['pk'])
        taken_quiz = TakenQuiz.objects.get(participant=participant, quiz=obj)

        return f'{taken_quiz.score()} %'


class MyQuizzesSerializer(ModelSerializer):
    answers = SerializerMethodField()
    progress = SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'progress', 'answers']

    def get_answers(self, obj):
        answers = ParticipantAnswer.objects.filter(participant=self.context['request'].user, question__quiz=obj)

        return AnswerWithQuestionSecretSerializer(answers, many=True).data

    def get_progress(self, obj):
        taken_quiz = TakenQuiz.objects.get(participant=self.context['request'].user, quiz=obj)

        return taken_quiz.progress()
