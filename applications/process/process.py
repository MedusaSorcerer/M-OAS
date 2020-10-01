#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import html
import json
import re

from django.core import serializers

from applications.user.models import UserModel
from lib import m_rest_framework as rest
from .models import ProcessModel


class SubmitProcessSerializerL(rest.ModelSerializer):
    organizer = rest.CharField(source='organizer.get_full_name')
    content = rest.SerializerMethodField(read_only=True)
    at_leader = rest.SerializerMethodField(read_only=True)

    def get_at_leader(self, obj):
        result = ''
        for i in UserModel.objects.filter(id__in=re.findall(r'"(\d+)"', obj.at_leader)):
            result += (i.get_full_name() + '、')
        return result[:-1]

    def get_content(self, obj):
        result = list()
        for i, value in enumerate(json.loads(obj.content)):
            if user := UserModel.objects.filter(id__exact=value[0]).first():
                username = f'{user.get_full_name()} ({user.username})'
            else:
                username = '未知用户'
            result.append([username, value[1], value[2], i])
        return result

    class Meta:
        model = ProcessModel
        fields = ('create_time', 'demand', 'id', 'organizer', 'protype', 'status', 'title', 'content', 'at_leader')


class SubmitProcessSerializerC(rest.ModelSerializer):
    class Meta:
        model = ProcessModel
        fields = ('title', 'at_leader', 'protype', 'demand', 'organizer', 'status')

    def validate_at_leader(self, val):
        at_leader = list(set(str(val).split(',')))
        try:
            if UserModel.objects.filter(id__in=at_leader).count() != len(at_leader):
                raise rest.ValidationError(detail='审核列表包含未识别的数据')
        except (Exception,):
            raise rest.ValidationError(detail='审核列表包含未识别的数据')
        resval = ''
        for i in at_leader:
            resval += f'"{i}"'
        return resval


class HandleProcessSerializerU(rest.Serializer):
    status = rest.ChoiceField(choices=('ok', 'no'))
    addreview = rest.CharField(allow_null=True, max_length=618)
    delhistory = rest.ListField()

    class Meta:
        fields = ('status', 'addreview', 'delhistory')


class ReviewProcessView(rest.UpdateModelMixin, rest.GenericViewSet):
    queryset = ProcessModel.objects.all()
    serializer_class = HandleProcessSerializerU

    def update(self, request, *args, **kwargs):
        if instance := self.queryset.filter(id__exact=kwargs.get('pk'), at_leader__regex=f'"{self.request.user.id}"').first():
            if instance.status not in [ProcessModel.OPEN, ProcessModel.DENY]:
                raise rest.NotFound
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            status, review, delindex = serializer.data.get('status'), serializer.data.get('addreview'), sorted(list(set(serializer.data.get('delhistory'))), reverse=True)
            if delindex == ['']: delindex = list()
            content = json.loads(instance.content)
            if delindex:
                if not all(x.isdigit() for x in delindex): raise rest.ParseError(detail='删除历史审批参数中包含不能识别的数据')
                if int(delindex[-1]) < 0: raise rest.ParseError(detail='删除历史审批参数中包含不能识别的数据')
                for i in delindex:
                    try:
                        if str(content[int(i)][0]) == str(request.user.id):
                            content.pop(int(i))
                        else:
                            print(content[int(i)][0])
                    except IndexError:
                        ...
            if review: content.append([request.user.id, status, html.escape(review)])
            instance.content = json.dumps(content)
            instance.save()
            update_instance = self.queryset.filter(id__exact=kwargs.get('pk')).first()
            state_ids = {i[0]: i[1] for i in json.loads(update_instance.content)}
            at_leader = re.findall(r'"(\d+)"', update_instance.at_leader)
            if len(set(at_leader)) == len(state_ids):
                if list(set(state_ids.values())) == ['ok']:
                    update_instance.status = ProcessModel.APPROVE
                else:
                    update_instance.status = ProcessModel.DENY
                update_instance.save()
            return rest.Response(data={'status': status, 'addreview': review, 'delhistory': delindex})
        raise rest.NotFound


class ProcessView(rest.DestroyModelMixin, rest.ListModelMixin, rest.CreateModelMixin, rest.GenericViewSet):
    queryset = ProcessModel.objects.all()
    pagination_class = rest.Pagination
    filter_backends = [rest.SearchFilter, rest.DjangoFilterBackend]
    search_fields = ['id', 'title']
    filterset_fields = ['status']

    def get_serializer_class(self):
        if 'submitProcess' in self.request.path:
            if self.request.method == 'GET':
                return SubmitProcessSerializerL
            return SubmitProcessSerializerC
        if 'handleProcess' in self.request.path:
            return SubmitProcessSerializerL

    def get_queryset(self):
        if 'handleProcess' in self.request.path:
            return self.queryset.filter(at_leader__regex=f'"{self.request.user.id}"')
        return self.queryset.filter(organizer__id__exact=self.request.user.id)

    def create(self, request, *args, **kwargs):
        data = request.data
        if hasattr(data, '_mutable'): data._mutable = True
        if data.get('at_leader'):
            data.update({'status': ProcessModel.OPEN, 'organizer': request.user.id})
        else:
            data.update({'status': ProcessModel.UNASSIGNED, 'organizer': request.user.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return rest.Response(data=serializer.data, status=rest.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        pks = list(set(kwargs.get('pk').split(',')))
        if '' in pks: pks.remove('')
        if ' ' in pks: pks.remove(' ')
        try:
            queryset = self.queryset.filter(id__in=pks)
        except ValueError:
            raise rest.ParseError(detail='包含无法解析的数据')
        if queryset.count() != len(pks): raise rest.ParseError(detail='包含无法解析的数据')
        queryset.update(status=ProcessModel.CLOSE)
        return rest.Response()


class AtLeaderView(rest.GenericViewSet, rest.ListModelMixin, rest.RetrieveModelMixin):
    queryset = ProcessModel.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = serializers.serialize('json', UserModel.objects.all(), fields=('username', 'id'))
        data = [{'value': i['pk'], 'name': i['fields']['username']} for i in json.loads(serializer)]
        return rest.Response(data=data)
