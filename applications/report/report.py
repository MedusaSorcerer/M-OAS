#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import html
import re
from datetime import datetime

from lib import m_rest_framework as rest
from .models import ReportModel


class ReportSerializer(rest.ModelSerializer):
    person = rest.SerializerMethodField()

    def get_person(self, obj):
        if username := obj.person:
            return f'{username.get_full_name()} ({username.username})'
        return ''

    class Meta:
        model = ReportModel
        fields = ('id', 'person', 'content', 'date', 'person_id')
        read_only_fields = ('id', 'person')


class ReportSerializerU(rest.ModelSerializer):
    class Meta:
        model = ReportModel
        fields = ('id', 'content', 'date')
        read_only_fields = ('id', 'date')


class ReportView(rest.GenericViewSet, rest.ListModelMixin, rest.UpdateModelMixin, rest.CreateModelMixin, rest.RetrieveModelMixin):
    queryset = ReportModel.objects.all()
    serializer_class = ReportSerializer

    def list(self, request, *args, **kwargs):
        date = datetime.now().strftime('%Y-%m-%d') if not request.query_params.get('date') else request.query_params.get('date')
        if not re.match(r'\d{4}-\d{2}-\d{2}', date): raise rest.ParseError(detail='时间格式错误，如 "2020-10-01" 格式')
        self.queryset = self.queryset.filter(
            date__year=date.split('-')[0], date__month=date.split('-')[1], date__day=date.split('-')[2]
        )
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ReportSerializerU
        if queryset := self.queryset.filter(id__exact=kwargs.get('pk')):
            if queryset.first().person.id != request.user.id:
                raise rest.ParseError(detail='你没有权限修改该日报')
        data = request.data
        if hasattr(data, '_mutable'): data._mutable = True
        data.update({'content': html.escape(data.get('content', ''))})
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        date = datetime.now().strftime('%Y-%m-%d')
        if self.queryset.filter(person_id__exact=request.user.id, date__year=date.split('-')[0], date__month=date.split('-')[1], date__day=date.split('-')[2]):
            raise rest.ParseError(detail='无法重复创建日报内容')
        data = {'person_id': request.user.id, 'content': html.escape(str(request.data.get('content', '')))}
        ReportModel.objects.create(**data)
        return rest.Response(data=data, status=rest.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        date = kwargs.get('pk')
        if not re.match(r'\d{4}-\d{2}-\d{2}', date): raise rest.ParseError(detail='时间格式错误，如 "2020-10-01" 格式')
        queryset = self.queryset.filter(date__year=date.split('-')[0], date__month=date.split('-')[1], date__day=date.split('-')[2], person_id__exact=request.user.id)
        if not queryset:
            return rest.Response(data={
                'id': None,
                'person': f'{request.user.get_full_name()} ({request.user.username})',
                'content': ''
            })
        return rest.Response(data={
            'id': queryset.first().id,
            'person': f'{request.user.get_full_name()} ({request.user.username})',
            'content': queryset.first().content
        })
