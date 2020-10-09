#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import datetime
import traceback

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import routers
from rest_framework import views, exceptions, response, viewsets, permissions, status, serializers, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.serializers import JSONWebTokenSerializer, RefreshJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

from applications.user.models import UserModel

AllowAny = permissions.AllowAny
NotAuthenticated = exceptions.NotAuthenticated
HTTP_401_UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
Serializer = serializers.Serializer
ModelSerializer = serializers.ModelSerializer
CharField = serializers.CharField
HTTP_201_CREATED = status.HTTP_201_CREATED
HTTP_204_NO_CONTENT = status.HTTP_204_NO_CONTENT
SearchFilter = filters.SearchFilter
ChoiceField = serializers.ChoiceField
NotFound = exceptions.NotFound
ListField = serializers.ListField
SerializerMethodField = serializers.SerializerMethodField
ValidationError = serializers.ValidationError
EmailField = serializers.EmailField
IntegerField = serializers.IntegerField
HTTP_200_OK = status.HTTP_200_OK


class APIView(views.APIView):
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if isinstance(user := request.user, UserModel):
            # field(last_login) -> field(last_activity_time)
            difference = datetime.datetime.now() - user.last_login
            if difference.days > 0 or difference.seconds >= 30 * 60:
                user.last_login = timezone.now()
                user.save()
        return self.response


class GenericAPIView(APIView, viewsets.generics.GenericAPIView):
    ...


class GenericViewSet(viewsets.ViewSetMixin, GenericAPIView):
    ...


class RetrieveModelMixin:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data)


class UpdateModelMixin:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(data=serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class ListModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            page_response = self.get_paginated_response(serializer.data)
            data = page_response.data
            result = data.pop('results')
            return Response(**data, data=result)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)


class DestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


class CreateModelMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError, AttributeError):
            return {}


class ParseError(exceptions.ParseError):
    def __init__(self, **kwargs):
        self.detail = {'msg': '', 'code': 0}
        self.detail.update(kwargs)


class Response(response.Response):
    def __init__(self, status=200, **kwargs):
        data = {'msg': '', 'code': 0, 'status': status}
        data.update(kwargs)
        super().__init__(data=data, status=status,
                         template_name=None, headers=None,
                         exception=False, content_type=None)


def custom_exception_handler(exc, context):
    res = views.exception_handler(exc, context)
    if res is not None:
        res.data['status_code'] = res.status_code
    else:
        traceback.print_exc()
        res = Response(detail='服务器异常', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return res


class Pagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_query_param = 'page'
    page_size_query_param = 'limit'


__all__ = [
    'HTTP_200_OK',
    'IntegerField',
    'EmailField',
    'ValidationError',
    'SerializerMethodField',
    'ListField',
    'NotFound',
    'ChoiceField',
    'DjangoFilterBackend',
    'SearchFilter',
    'HTTP_204_NO_CONTENT',
    'DestroyModelMixin',
    'HTTP_201_CREATED',
    'CreateModelMixin',
    'Pagination',
    'custom_exception_handler',
    'routers',
    'RetrieveModelMixin',
    'ListModelMixin',
    'CharField',
    'ModelSerializer',
    'Serializer',
    'HTTP_401_UNAUTHORIZED',
    'NotAuthenticated',
    'RefreshJSONWebTokenSerializer',
    'AllowAny',
    'GenericViewSet',
    'api_settings',
    'Response',
    'ParseError',
    'JSONWebTokenSerializer',
    'JSONWebTokenAPIView',
    'APIView',
]
