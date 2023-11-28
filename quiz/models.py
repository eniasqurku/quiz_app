from numbers import Number

from django.db import models

from agent.models import User


class UpdateCreateDate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Quiz(UpdateCreateDate):
    title = models.CharField(max_length=50, verbose_name="Quiz title")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ["id"]

    @property
    def question_count(self):
        return self.questions.count()


class Question(UpdateCreateDate):
    title = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["id"]

    def __str__(self):
        return self.title


class Option(UpdateCreateDate):
    title = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Options"
        ordering = ["id"]

    def __str__(self):
        return f"{self.question} - {self.title} - {self.correct}"


class ParticipantAnswer(models.Model):
    participant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="answers")

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        unique_together = ("participant", "question")

    def is_correct(self) -> bool:
        return self.answer.correct

    def can_answer(self) -> bool:
        """
        check if the chosen question belongs to any of the taken quiz by the participant
        and that the option he/she chooses belongs to the question in speak
        """
        return (
            self.question.quiz_id
            in self.participant.attempted_quizzes.all().values_list("quiz", flat=True)
            and self.answer.question == self.question
        )


class QuizAttempt(models.Model):
    participant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="attempted_quizzes"
    )
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="attempted_quizzes"
    )

    class Meta:
        unique_together = ["participant", "quiz"]
        ordering = ["id"]

    @property
    def progress(self) -> str:
        return f"{ParticipantAnswer.objects.filter(participant=self.participant, question__quiz=self.quiz).count()} / {self.quiz.question_count}"

    @property
    def score(self) -> Number:
        if self.quiz.question_count == 0:
            return 0

        answers = ParticipantAnswer.objects.filter(
            participant=self.participant, question__quiz=self.quiz
        )
        corrects_answers = 0
        for answer in answers:
            if answer.is_correct():
                corrects_answers += 1

        return (corrects_answers / self.quiz.question_count) * 100

    def __str__(self):
        return f"{self.participant} - {self.quiz}"
