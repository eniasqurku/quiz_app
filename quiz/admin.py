from django.contrib import admin
from django.contrib.admin import ModelAdmin

from quiz.models import Quiz, Question, ParticipantAnswer, TakenQuiz


class AdminQuiz(ModelAdmin):
    list_display = ('title', 'owner')
    list_filter = ("title", "owner")
    search_fields = ("title", "owner__email", "owner__first_name", "owner__last_name")


class AdminQuestion(ModelAdmin):
    list_display = ('title', 'quiz', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_answer')
    list_filter = ("title", "quiz", "correct_answer")
    search_fields = ("title", "quiz__title")


class AdminAnswer(ModelAdmin):
    list_display = ('participant', 'question', 'answer')
    list_filter = ('participant', 'question', 'answer')
    search_fields = ('participant__email', 'question__title', 'answer')


class AdminTakenQuiz(ModelAdmin):
    list_display = ('participant', 'quiz')
    list_filter = ('participant', 'quiz')
    search_fields = ('participant__email', 'quiz__title')


class CustomAdmin(ModelAdmin):
    change_list_template = 'custom.html'


admin.site.register(Quiz, AdminQuiz)
admin.site.register(Question, AdminQuestion)
admin.site.register(ParticipantAnswer, AdminAnswer)
admin.site.register(TakenQuiz, AdminTakenQuiz)
