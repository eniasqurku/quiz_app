from django.db import migrations

from agent.cons import CREATOR_GROUP_NAME, PARTICIPANT_GROUP_NAME


def update_allowed_variabilities(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Groups = apps.get_model("auth", "Group")
    Groups.objects.using(db_alias).create(name=CREATOR_GROUP_NAME)
    Groups.objects.using(db_alias).create(name=PARTICIPANT_GROUP_NAME)


class Migration(migrations.Migration):
    dependencies = [
        ("agent", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            update_allowed_variabilities, reverse_code=migrations.RunPython.noop
        ),
    ]
