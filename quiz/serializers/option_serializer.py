from django.utils.functional import cached_property
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from quiz.models import Option, Question
from quiz_app.common.utils import is_creator


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "title", "correct"]

    @cached_property
    def fields(self):
        fields = super().fields

        if not is_creator(self.context["request"].user):
            fields.pop("correct")

        return fields

    def create(self, validated_data):
        question_id = self.context["view"].kwargs["question_id"]
        question = get_object_or_404(Question, pk=question_id)

        if question.quiz.owner != self.context["request"].user:
            raise ValidationError(
                "You do not have permission to create options for this question",
                code=status.HTTP_403_FORBIDDEN,
            )
        validated_data["question"] = question

        return super().create(validated_data)
