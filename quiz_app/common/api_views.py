import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.transaction import atomic
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from quiz_app.common.action_logger import ADDITION, log_addition, CHANGE, log_change, DELETION, log_deletion, READ, \
    log_read
from quiz_app.common.api_permissions import CanAdd, CanChange, CanDelete
from quiz_app.cons import DATA, ERROR_TYPE, VALIDATION_ERROR, ERRORS, MESSAGE, HTTP_404, INTEGRITY_ERROR, INVALID_DATA, \
    OTHER
from quiz_app.exceptions import InvalidData, APIException202

logger = logging.getLogger(__name__)


class MyListAPIView(ListAPIView):
    queryset = None
    serializer_class = None
    filter_serializer_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        track_action(request.user, serializer, READ)
        return Response(serializer.data)


class MyCreateAPIView(CreateAPIView):

    @atomic
    @permission_classes([CanAdd])
    def create(self, request, *args, **kwargs):
        data = {}
        if 'data' in request.data:  # POST request with FILES
            for key in request.FILES.keys():
                data[key] = request.FILES[key]
            post_data = json.loads(request.data['data'])
            data.update(post_data)
        else:  # SIMPLE POST request
            data = request.data
        serializer = self.get_serializer(data=data)

        response_data = {}
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_headers = None
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response_data = {DATA: serializer.data}
            response_status = status.HTTP_201_CREATED
            response_headers = headers
            track_action(request.user, serializer, ADDITION)
        except ValidationError as ve:
            logger.error('Create Error: {}'.format(ve))
            error_dict = ve.get_full_details()
            response_data = {
                ERROR_TYPE: VALIDATION_ERROR,
                ERRORS: error_dict,
                MESSAGE: get_validation_error_message(error_dict)
            }
            response_status = status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist as dne:
            logger.error('Object does not exist Error: {}'.format(dne))
            response_data = {
                ERROR_TYPE: HTTP_404,
                ERRORS: '{}'.format(dne),
                MESSAGE: 'Does not exist',
            }
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        except IntegrityError as ie:
            logger.error('{}'.format(ie))
            response_data = {
                ERROR_TYPE: INTEGRITY_ERROR,
                ERRORS: '{}'.format(ie),
                MESSAGE: 'Database error',
            }
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        except InvalidData as ex:
            response_data = {
                ERROR_TYPE: INVALID_DATA,
                ERRORS: ex.get_message(),
                MESSAGE: ex.get_message(),
            }
            response_status = status.HTTP_400_BAD_REQUEST
        except APIException202 as ae:
            headers = self.get_success_headers(serializer.data)
            response_data = {DATA: ae.obj, MESSAGE: ae.message}
            response_status = status.HTTP_202_ACCEPTED
            response_headers = headers
        except Exception as e:
            response_data = {
                ERROR_TYPE: OTHER,
                ERRORS: '{}'.format(e),
                MESSAGE: 'Server problem'
            }
        finally:
            return Response(response_data, status=response_status, headers=response_headers)


class MyListCreateAPIView(MyCreateAPIView, MyListAPIView):
    list_read_serializer_class = None
    read_serializer_class = None
    write_serializer_class = None
    filter_serializer_class = None
    serializer_error_msg = "'%s' should either include a `serializer_class` attribute, or override the " \
                           "`get_serializer_class()` method."
    queryset = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.list_read_serializer_class is not None:
                return self.list_read_serializer_class
            assert self.read_serializer_class is not None or self.serializer_class is not None, (
                    self.serializer_error_msg % self.__class__.__name__)
            return self.read_serializer_class
        if self.request.method == 'POST':
            assert self.write_serializer_class is not None or self.serializer_class is not None, (
                    self.serializer_error_msg % self.__class__.__name__)
            return self.write_serializer_class
        assert self.serializer_class is not None, (self.serializer_error_msg % self.__class__.__name__)
        return self.serializer_class


class MyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an object instance.
    """
    queryset = None
    serializer_class = None
    read_serializer_class = None
    write_serializer_class = None
    serializer_error_msg = "'%s' should either include a `serializer_class` attribute, or override the " \
                           "`get_serializer_class()` method."
    delete_obj_id_physical = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            assert self.read_serializer_class is not None or self.serializer_class is not None, (
                    self.serializer_error_msg % self.__class__.__name__)
            return self.read_serializer_class
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'PATCH':
            assert self.write_serializer_class is not None or self.serializer_class is not None, (
                    self.serializer_error_msg % self.__class__.__name__)
            return self.write_serializer_class
        assert self.serializer_class is not None, (self.serializer_error_msg % self.__class__.__name__)
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            track_action(request.user, instance, READ)
            return Response({DATA: serializer.data})
        except Http404 as e:
            response_data = {
                ERROR_TYPE: HTTP_404,
                ERRORS: '{}'.format(e),
                MESSAGE: 'Not found'
            }
            response_status = status.HTTP_404_NOT_FOUND
            return Response(response_data, status=response_status)

    @atomic
    @permission_classes([CanChange])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = {}
        if 'data' in request.data:  # POST request with FILES
            for key in request.FILES.keys():
                data[key] = request.FILES[key]
            post_data = json.loads(request.data['data'])
            data.update(post_data)
        else:  # SIMPLE POST request
            data = request.data
        serializer = self.get_serializer(instance, data=data, partial=partial)

        response_data = {}
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            response_data = {DATA: serializer.data}
            response_status = status.HTTP_200_OK
            track_action(request.user, serializer, CHANGE)
        except ValidationError as ve:
            logger.error('Create Error: {}'.format(ve))
            error_dict = ve.get_full_details()
            response_data = {
                ERROR_TYPE: VALIDATION_ERROR,
                ERRORS: error_dict,
                MESSAGE: get_validation_error_message(error_dict)
            }
            response_status = status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist as dne:
            logger.error('Object does not exist Error: {}'.format(dne))
            response_data = {
                ERROR_TYPE: HTTP_404,
                ERRORS: '{}'.format(dne),
                MESSAGE: 'Does not exists',
            }
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        except IntegrityError as ie:
            logger.error('{}'.format(ie))
            response_data = {
                ERROR_TYPE: INTEGRITY_ERROR,
                ERRORS: '{}'.format(ie),
                MESSAGE: 'Database error',
            }
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        except InvalidData as ex:
            response_data = {
                ERROR_TYPE: INVALID_DATA,
                ERRORS: ex.get_message(),
                MESSAGE: ex.get_message(),
            }
            response_status = status.HTTP_400_BAD_REQUEST
        except APIException202 as ae:
            response_data = {DATA: ae.obj, MESSAGE: ae.message}
            response_status = status.HTTP_202_ACCEPTED
        except Exception as e:
            response_data = {
                ERROR_TYPE: OTHER,
                ERRORS: '{}'.format(e),
                MESSAGE: 'Server problem'
            }
        finally:
            return Response(response_data, status=response_status)

    @permission_classes([CanDelete])
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # if hasattr(instance, 'deleted'):
            #     instance.deleted = True
            #     instance.save()
            # else:
            #     self.perform_destroy(instance)
            self.perform_destroy(instance)
            track_action(request.user, instance, DELETION)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404 as e:
            response_data = {
                ERROR_TYPE: HTTP_404,
                ERRORS: '{}'.format(e),
                MESSAGE: 'Missing'
            }
            response_status = status.HTTP_404_NOT_FOUND
            return Response(response_data, status=response_status)


def get_validation_error_message(error_data):
    try:
        response_message = ''
        if isinstance(error_data, dict):
            for key, value in error_data.items():
                for item in value:
                    if 'message' in item:
                        response_message += '{}: {} '.format(key, item['message'])
                    else:
                        if isinstance(item, dict):
                            for unit_key, unit_value in item.items():
                                for arr_item in unit_value:
                                    response_message += '{}: {} '.format(unit_key, arr_item['message'])
                        elif isinstance(item, str):
                            for item_key, item_val in value.items():
                                for arr_item in item_val:
                                    response_message += '{}: {} '.format(item_key, arr_item['message'])
        elif isinstance(error_data, list):
            for arr_item in error_data:
                response_message += '{} '.format(arr_item['message'])
    except:
        response_message = 'Error {}'.format(error_data)
    return response_message


def track_action(user, serializer, action):
    action_user_id = None if user.is_anonymous else user.id
    if hasattr(serializer, 'instance'):
        model_obj = serializer.instance
    else:
        model_obj = serializer
    if action == ADDITION:
        log_addition(action_user_id, model_obj)
    elif action == CHANGE:
        log_change(action_user_id, model_obj)
    elif action == DELETION:
        log_deletion(action_user_id, model_obj)
    elif action == READ:
        log_read(action_user_id, model_obj)
