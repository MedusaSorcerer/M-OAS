#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import html
import re
from datetime import datetime

from lib import m_rest_framework as rest
from .models import ReportModel, MonthlyReportModel, SubjectModel, VersionManagement


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
    permission = {'m/4/1': '__all__'}

    def list(self, request, *args, **kwargs):
        date = datetime.now().strftime('%Y-%m-%d') if not request.query_params.get('date') else request.query_params.get('date')
        if not re.match(r'\d{4}-\d{2}-\d{2}', date): raise rest.ParseError(detail='时间格式错误，如 "2020-10-01" 格式')
        self.queryset = self.queryset.filter(
            date__year=date.split('-')[0], date__month=date.split('-')[1], date__day=date.split('-')[2], person__department_id=request.user.department_id,
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


class MonthlyReportSerializer(rest.ModelSerializer):
    submitter = rest.SerializerMethodField()
    department_name = rest.SerializerMethodField()

    def get_department_name(self, obj):
        if obj.person and (department := obj.person.department):
            return department.name
        return ''

    def get_submitter(self, obj):
        if username := obj.person:
            return f'{username.get_full_name()} ({username.username})'
        return ''

    class Meta:
        model = MonthlyReportModel
        fields = ('id', 'person', 'department', 'content', 'date', 'update', 'submitter', 'department_name')
        read_only_fields = ('id', 'update', 'submitter', 'department_name')


class MonthlyReportSerializerU(rest.ModelSerializer):
    class Meta:
        model = MonthlyReportModel
        fields = ('content', 'person')


class MonthlyReportView(rest.GenericViewSet, rest.ListModelMixin, rest.UpdateModelMixin, rest.CreateModelMixin, rest.RetrieveModelMixin):
    serializer_class = MonthlyReportSerializer
    queryset = MonthlyReportModel.objects.all()
    permission = {'m/4/2': '__all__'}

    def update(self, request, *args, **kwargs):
        self.serializer_class = MonthlyReportSerializerU
        if hasattr(request.data, '_mutable'): request.data._mutable = True
        request.data['person'] = request.user.id
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not request.user.department_id: raise rest.PermissionDenied
        data = {
            'person': request.user.id,
            'content': request.data.get('content'),
            'date': request.data.get('date'),
            'department': request.user.department_id,
        }
        if not re.search(r'^20\d\d(0[1-9]|1[0-2])$', data.get('date')): raise rest.ParseError(detail='填报日期格式错误')
        if self.queryset.filter(date__exact=data.get('date'), department_id__exact=data.get('department')):
            raise rest.ParseError(detail='无法重复创建月报内容')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return rest.Response(data=serializer.data, status=rest.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.department_id: raise rest.PermissionDenied
        instance = self.queryset.filter(date__exact=kwargs.get('pk'), department_id__exact=request.user.department_id).first()
        if not instance:
            return rest.Response(data={
                'id': None,
                'submitter': f'{request.user.get_full_name()} ({request.user.username})',
                'content': '',
            })
        serializer = self.get_serializer(instance)
        return rest.Response(data=serializer.data)

    def list(self, request, *args, **kwargs):
        date = datetime.now().strftime('%Y%m') if not request.query_params.get('date') else request.query_params.get('date')
        self.queryset = self.queryset.filter(date__exact=date)
        return super().list(request, *args, **kwargs)


class SubjectSerializer(rest.ModelSerializer):
    pertain_info = rest.SerializerMethodField()
    last_version = rest.SerializerMethodField()

    def get_last_version(self, obj):
        if obj := obj.versionmanagement_set.all().order_by('-create'):
            return obj.first().version

    def get_pertain_info(self, obj):
        if username := obj.pertain:
            return f'{username.get_full_name()} ({username.username})'
        return ''

    class Meta:
        model = SubjectModel
        fields = ('id', 'name', 'schedule', 'team', 'update', 'pertain_info', 'description', 'establish', 'accomplish', 'last_version', 'pertain')
        read_only_fields = ('update', 'pertain_info', 'last_version')


class SubjectView(rest.GenericViewSet, rest.ListModelMixin, rest.UpdateModelMixin, rest.DestroyModelMixin, rest.RetrieveModelMixin, rest.CreateModelMixin):
    queryset = SubjectModel.objects.all()
    serializer_class = SubjectSerializer
    permission = {'m/4/3': '__all__'}

    def update(self, request, *args, **kwargs):
        if obj := self.queryset.filter(id__exact=kwargs.get('pk')):
            if obj.first().pertain_id != request.user.id:
                raise rest.PermissionDenied
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if obj := self.queryset.filter(id__exact=kwargs.get('pk')):
            if obj.first().pertain_id != request.user.id:
                raise rest.PermissionDenied
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'schedule': request.data.get('schedule'),
            'team': request.data.get('team'),
            'description': request.data.get('description'),
            'establish': request.data.get('establish'),
            'accomplish': request.data.get('accomplish'),
            'pertain': request.user.id,
        }
        if hasattr(request.data, '_mutable'): request.data._mutable = True
        request.data.update(data)
        return super().create(request, *args, **kwargs)


class VersionManagementSerializer(rest.ModelSerializer):
    def validate_document(self, val):
        if val: return html.escape(val)
        return val

    class Meta:
        model = VersionManagement
        fields = ('version', 'document', 'id')
        read_only_fields = ('subject',)


class VersionManagementSerializerC(rest.ModelSerializer):
    id = rest.IntegerField(source='subject_id', required=True)

    def validate_document(self, val):
        if val: return html.escape(val)
        return val

    class Meta:
        model = VersionManagement
        fields = ('version', 'document', 'id')


class VersionManagementView(rest.GenericViewSet, rest.RetrieveModelMixin, rest.DestroyModelMixin, rest.CreateModelMixin, rest.UpdateModelMixin):
    queryset = VersionManagement.objects.all()
    serializer_class = VersionManagementSerializer
    permission = {'m/4/3': '__all__'}

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset.filter(subject_id__exact=kwargs.get('pk')).order_by('-create')
        serializer = self.get_serializer(queryset, many=True)
        return rest.Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        if obj := self.queryset.filter(id__exact=kwargs.get('pk')):
            if obj.first().subject.pertain_id != request.user.id:
                raise rest.PermissionDenied
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if obj := self.queryset.filter(id__exact=kwargs.get('pk')):
            if obj.first().subject.pertain_id != request.user.id:
                raise rest.PermissionDenied
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = VersionManagementSerializerC
        if obj := SubjectModel.objects.filter(id__exact=request.data.get('id')):
            if obj.first().pertain_id != request.user.id:
                raise rest.PermissionDenied
        else:
            raise rest.NotFound
        return super().create(request, *args, **kwargs)
