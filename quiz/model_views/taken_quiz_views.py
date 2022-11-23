from quiz.model_serializers.taken_quiz_serializers import TakenQuizSerializer
from quiz.models import TakenQuiz
from quiz_app.common.api_permissions import IsParticipant
from quiz_app.common.api_views import MyCreateAPIView


class Participate(MyCreateAPIView):
    queryset = TakenQuiz.objects.all()
    serializer_class = TakenQuizSerializer
    permission_classes = [IsParticipant]
