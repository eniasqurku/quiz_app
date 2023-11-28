from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from agent.models import User
from agent.utils import send_invitation_email, send_score_email
from quiz.models import Quiz, QuizAttempt
from quiz_app.common.api_permissions import IsCreator
from quiz_app.cons import MESSAGE, ERRORS


@api_view(["POST"])
@permission_classes([IsCreator])
def invite_participant(request):
    """
    Invite user to participate in quiz through email

    Body Parameter:
        quiz: int
        email: str
    """
    quiz_id = request.data["quiz"]
    email = request.data["email"]
    send_invitation_email(email, quiz_id)

    return Response(
        {MESSAGE: "Invitation sent successfully"}, status=status.HTTP_204_NO_CONTENT
    )


@api_view(["POST"])
@permission_classes([IsCreator])
def notify(request, pk):
    """
    Send email to user with the results of their quiz

    Body Parameter:
        quiz: int
    """
    quiz_id = request.data.get("quiz")
    if not quiz_id:
        return Response(
            {ERRORS: "Please supply 'quiz' parameter in the body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    participant = get_object_or_404(User, pk=pk)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user = request.user
    if quiz not in user.quizzes.all():
        return Response(
            {ERRORS: "You don't have permission to notify about other quizzes"},
            status=status.HTTP_403_FORBIDDEN,
        )
    quiz_attempt = QuizAttempt.objects.filter(
        participant=participant, quiz=quiz
    ).first()
    if quiz_attempt:
        data = {"quiz": quiz_attempt.quiz.title, "score": quiz_attempt.score}
        send_score_email(participant.email, data)
        return Response({MESSAGE: "Successful"}, status=status.HTTP_204_NO_CONTENT)

    return Response(
        {MESSAGE: "User has not taken the specified quiz"},
        status=status.HTTP_400_BAD_REQUEST,
    )
