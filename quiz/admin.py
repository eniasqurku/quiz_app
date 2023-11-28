from django.contrib import admin
from django.contrib.admin import ModelAdmin

from quiz.models import Quiz, Question, ParticipantAnswer, QuizAttempt, Option


class QuizQuestions(admin.TabularInline):
    model = Question


class AdminQuiz(ModelAdmin):
    inlines = (QuizQuestions,)
    list_display = ("title", "owner")
    list_filter = ("title", "owner")
    search_fields = ("title", "owner__email", "owner__first_name", "owner__last_name")


class QuestionOptions(admin.TabularInline):
    model = Option


class AdminQuestion(ModelAdmin):
    inlines = (QuestionOptions,)

    list_display = (
        "title",
        "quiz",
    )
    list_filter = ("title", "quiz")
    search_fields = ("title", "quiz__title")


class AdminAnswer(ModelAdmin):
    list_display = ("participant", "question", "answer")
    list_filter = ("participant", "question", "answer")
    search_fields = ("participant__email", "question__title", "answer")


class AdminQuizAttempt(ModelAdmin):
    list_display = ("participant", "quiz")
    list_filter = ("participant", "quiz")
    search_fields = ("participant__email", "quiz__title")


admin.site.register(Quiz, AdminQuiz)
admin.site.register(Question, AdminQuestion)
admin.site.register(Option)
admin.site.register(ParticipantAnswer, AdminAnswer)
admin.site.register(QuizAttempt, AdminQuizAttempt)
