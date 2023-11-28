# Generated by Django 4.1.13 on 2023-11-28 00:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="option",
            options={
                "ordering": ["id"],
                "verbose_name": "Option",
                "verbose_name_plural": "Options",
            },
        ),
        migrations.AlterModelOptions(
            name="question",
            options={
                "ordering": ["id"],
                "verbose_name": "Question",
                "verbose_name_plural": "Questions",
            },
        ),
        migrations.RenameField(
            model_name="participantanswer",
            old_name="option",
            new_name="answer",
        ),
    ]
