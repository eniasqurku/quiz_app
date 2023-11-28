from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import BasePermission

from agent.cons import CREATOR_GROUP_ID, PARTICIPANT_GROUP_ID


class CanView(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        obj = ContentType.objects.get_for_model(view.queryset.model)
        return user and user.has_perm(obj.app_label + ".view_" + obj.model)


class CanAdd(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        obj = ContentType.objects.get_for_model(view.queryset.model)
        return user and user.has_perm(obj.app_label + ".add_" + obj.model)


class CanChange(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        obj = ContentType.objects.get_for_model(view.queryset.model)
        return user and user.has_perm(obj.app_label + ".change_" + obj.model)


class CanDelete(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        obj = ContentType.objects.get_for_model(view.queryset.model)
        return user and user.has_perm(obj.app_label + ".delete_" + obj.model)


class IsCreator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser or user.groups.filter(id=CREATOR_GROUP_ID)


class IsParticipant(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser or user.groups.filter(id=PARTICIPANT_GROUP_ID)
