from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from agent.filters.agent_filters import UserFilter
from agent.model_serializers.agent_serializers import UserReadSerializer, UserQuizzesSerializer, MyQuizzesSerializer
from agent.models import User
from agent.utils import send_invitation_email, send_score_email
from quiz.filters.quiz_filters import QuizFilter
from quiz.models import Quiz, TakenQuiz
from quiz_app.common.api_permissions import IsCreator, IsParticipant
from quiz_app.common.api_views import MyListAPIView
from quiz_app.cons import MESSAGE, ERRORS


class ParticipantListAPIView(MyListAPIView):
    serializer_class = UserReadSerializer
    filterset_class = UserFilter
    permission_classes = [IsCreator]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(user_quizzes__quiz__in=user.quizzes.all())


class UserQuizzes(MyListAPIView):
    serializer_class = UserQuizzesSerializer
    filterset_class = QuizFilter
    permission_classes = [IsCreator]

    def get_queryset(self):
        users = User.objects.all()
        participant = get_object_or_404(users, pk=self.kwargs['pk'])

        return Quiz.objects.filter(user_quizzes__participant=participant, owner=self.request.user)


class MyQuizzes(MyListAPIView):
    serializer_class = MyQuizzesSerializer
    filterset_class = QuizFilter
    permission_classes = [IsParticipant]

    def get_queryset(self):
        return Quiz.objects.filter(user_quizzes__participant=self.request.user)


@api_view(['POST'])
def invite_participant(request):
    """
    Invite user with given email to participate in given quiz

    Body Parameter:
        quiz: int
        email: str
    """
    quiz_id = request.data['quiz']
    email = request.data['email']
    send_invitation_email(email, quiz_id)

    return Response({MESSAGE: 'Invitation sent successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsCreator])
def notify(request, pk):
    """
    Notify user with given id of the results of given quiz

    Body Parameter:
        quiz: int
    """
    quiz_id = request.data['quiz']
    participant = get_object_or_404(User.objects.all(), pk=pk)
    quiz = get_object_or_404(Quiz.objects.all(), pk=quiz_id)
    user = request.user
    if quiz not in user.quizzes.all():
        return Response({ERRORS: "You don't have permission to notify about other quizzes"},
                        status=status.HTTP_403_FORBIDDEN)
    taken_quiz = TakenQuiz.objects.filter(participant=participant, quiz=quiz).first()
    if taken_quiz:
        data = (taken_quiz.quiz.title, taken_quiz.score())
        send_score_email(participant.email, data)
        return Response({MESSAGE: 'Successful'}, status=status.HTTP_204_NO_CONTENT)

    return Response({MESSAGE: 'User has not taken the specified quiz'}, status=status.HTTP_400_BAD_REQUEST)
