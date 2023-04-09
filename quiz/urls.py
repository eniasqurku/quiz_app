from django.urls import path

from quiz.views.answer_views import AnswerListCreateAPIView, AnswerRetrieveUpdateDestroyView
from quiz.views.question_views import QuestionListCreateAPIView, QuestionRetrieveUpdateDestroyView
from quiz.views.quiz_views import QuizListCreateAPIView, QuizRetrieveUpdateDestroyView
from quiz.views.taken_quiz_views import Participate

urlpatterns = [
    path('quizzes/', QuizListCreateAPIView.as_view(), name='quizzes'),
    path('quizzes/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view(), name='quiz'),

    path('answer/', AnswerListCreateAPIView.as_view(), name='answers'),
    path('answer/<int:pk>/', AnswerRetrieveUpdateDestroyView.as_view(), name='answer'),

    path('questions/', QuestionListCreateAPIView.as_view(), name='questions'),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question'),

    path('participate/', Participate.as_view(), name='participate'),

]
