from django.contrib.contenttypes.models import ContentType

from common.models import ActionLogger

ADDITION = 1
CHANGE = 2
DELETION = 3
READ = 4


def log_addition(user_id, model_object):
    log_action(
        user_id,
        model_object,
        ADDITION,
        "Create: {}".format(model_object._meta.verbose_name.title()),
    )


def log_read(user_id, model_object):
    log_action(
        user_id,
        model_object,
        READ,
        "Read: {}".format(model_object._meta.verbose_name.title()),
    )


def log_change(user_id, model_object):
    log_action(
        user_id,
        model_object,
        CHANGE,
        "Update: {}".format(model_object._meta.verbose_name.title()),
    )


def log_change_registration_state(user_id, model_object, state):
    log_action(
        user_id,
        model_object,
        state,
        "Update: {}".format(model_object._meta.verbose_name.title()),
    )


def log_deletion(user_id, model_object):
    log_action(
        user_id,
        model_object,
        DELETION,
        "Delete: {}".format(model_object._meta.verbose_name.title()),
    )


def log_action(user_id, model_object, action, message):
    try:
        pk = model_object.id
    except AttributeError:
        pk = model_object.pk
    ActionLogger.objects.log_action(
        user_id=user_id,
        content_type_id=ContentType.objects.get_for_model(model_object._meta.model).id,
        object_id=pk,
        object_repr=model_object._meta.verbose_name.title(),
        action_flag=action,
        change_message=message,
    )


def log_action_no_model(user_id, model_object, action, message):
    ActionLogger.objects.log_action(
        user_id=user_id,
        content_type_id=ContentType.objects.get_for_model(model_object._meta.model).id,
        object_id=model_object.id,
        object_repr=model_object._meta.verbose_name.title(),
        action_flag=action,
        change_message=message,
    )
