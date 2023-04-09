from django.db import models

from agent.models import User

OPTIONS = (
    (1, 'Option 1'),
    (2, 'Option 2'),
    (3, 'Option 3'),
    (4, 'Option 4')
)


class UpdateCreateDate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Quiz(UpdateCreateDate):
    title = models.CharField(max_length=50, verbose_name='Quiz title')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = 'Quizzes'
        ordering = ['id']

    @property
    def question_count(self):
        return self.questions.count()


class Question(UpdateCreateDate):
    title = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    correct_answer = models.IntegerField(choices=OPTIONS)

    def __str__(self):
        return self.title


class ParticipantAnswer(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.IntegerField(choices=OPTIONS)

    def is_correct(self):
        return self.question.correct_answer == self.answer

    def can_answer(self):
        return self.question.quiz_id in self.participant.user_quizzes.all().values_list('quiz', flat=True)


class TakenQuiz(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='user_quizzes')

    class Meta:
        unique_together = ["participant", "quiz"]

    def progress(self):
        return f'{ParticipantAnswer.objects.filter(participant=self.participant, question__quiz=self.quiz).count()} / {self.quiz.question_count} '

    def score(self):
        answers = ParticipantAnswer.objects.filter(participant=self.participant, question__quiz=self.quiz)
        corrects_answers = 0
        for answer in answers:
            if answer.is_correct():
                corrects_answers += 1

        return (corrects_answers / self.quiz.question_count) * 100

    def __str__(self):
        return f"{self.participant.email} - {self.quiz.title}"
