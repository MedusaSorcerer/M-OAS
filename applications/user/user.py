#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import base64
import json
import os
import re
import uuid

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AnonymousUser
from django.core import serializers
from django.db.models import Q

from MOAS import settings
from lib import m_rest_framework as rest
from .models import UserModel, DepartmentModel, RoleModel
from .views import workplace as get_workplace, navs, format_role

jwt_response_payload_handler = rest.api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


def rsa_decrypt(_):
    with open(os.path.join(settings.BASE_DIR, 'applications', 'user', 'private.pem')) as file:
        key = file.read().encode()
        file.close()
    cipher = PKCS1_v1_5.new(RSA.importKey(key))
    return cipher.decrypt(base64.b64decode(_.encode()), 'error').decode()


class LoginView(rest.JSONWebTokenAPIView):
    serializer_class = rest.JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        username, password = request.data.get('username'), request.data.get('password')
        queryset = UserModel.objects.filter(username__exact=username)
        if not queryset: raise rest.ParseError(detail='账号或密码错误')
        try:
            password = rsa_decrypt(password)
        except (ValueError, AttributeError):
            raise rest.ParseError(detail='账号或密码错误')
        serializer = self.get_serializer(data={'username': username, 'password': password})
        if serializer.is_valid():
            token = serializer.object.get('token')
            user = serializer.object.get('user') if isinstance(request.user, AnonymousUser) else request.user
            if not user: user = serializer.object.get('username')
            return rest.Response(data=jwt_response_payload_handler(token, user, request))
        raise rest.ParseError(detail='账号或密码错误')


class PublicKeyView(rest.GenericViewSet):
    permission_classes = [rest.AllowAny]

    def list(self, request, *args, **kwargs):
        with open(os.path.join(settings.BASE_DIR, 'applications', 'user', 'public.pem')) as file:
            pub = file.read()
            file.close()
        if not pub: raise rest.ParseError(detail='获取密钥信息失败')
        return rest.Response(data=pub)


class LogoutView(rest.APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        user.user_secret = uuid.uuid4()
        user.save()
        return rest.Response(detail='退出登录')


class RefreshAPIView(rest.JSONWebTokenAPIView):
    serializer_class = rest.RefreshJSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        import applications.user.models
        serializer = self.get_serializer(data=request.data)
        try:
            is_valid = serializer.is_valid()
        except applications.user.models.UserModel.DoesNotExist:
            raise rest.NotAuthenticated
        if is_valid:
            user, token = (serializer.object.get('user') or request.user), serializer.object.get('token')
            return rest.Response((token, user, request))
        return rest.Response(detail='会话已过期', status=rest.HTTP_401_UNAUTHORIZED)


class UserChangeSerializer(rest.Serializer):
    old = rest.CharField(allow_null=False, allow_blank=False)
    new = rest.CharField(allow_null=False, allow_blank=False, max_length=12, min_length=6)
    again = rest.CharField(allow_null=False, allow_blank=False, max_length=12, min_length=6)


class UserChangeViewSet(rest.APIView):
    queryset = UserModel.objects.all()
    serializer_class = UserChangeSerializer

    def put(self, request, *args, **kwargs):
        try:
            old, new, again = (
                rsa_decrypt(request.data.get('old')),
                rsa_decrypt(request.data.get('new')),
                rsa_decrypt(request.data.get('again'))
            )
        except (ValueError, AttributeError):
            raise rest.ParseError(detail='原密码错误')
        if not check_password(old, request.user.password): raise rest.ParseError(detail='原密码错误')
        serializer = self.serializer_class(data={'old': old, 'new': new, 'again': again})
        if serializer.is_valid():
            if new != again: raise rest.ParseError(detail='两次输入的密码不一致')
            user = request.user
            user.user_secret = uuid.uuid4()
            user.password = make_password(new)
            user.save()
            return rest.Response(detail='密码修改成功，请重新登录')
        raise rest.ParseError(detail='会话已过期')


class UserNavsView(rest.APIView):
    def get(self, request, *args, **kwargs):
        return rest.Response(data=navs(request.user.role.role if request.user.role else '[]'))


class UserSerializerL(rest.ModelSerializer):
    department = rest.SerializerMethodField()
    role = rest.SerializerMethodField()

    def get_department(self, obj):
        if obj.department: return obj.department.name

    def get_role(self, obj):
        if obj := obj.role: return obj.name

    class Meta:
        model = UserModel
        fields = ('id', 'get_full_name', 'username', 'email', 'is_active', 'department', 'date_joined', 'role')


class UserSerializerR(rest.ModelSerializer):
    workplace = rest.SerializerMethodField()
    role = rest.IntegerField(source='role_id')

    def get_workplace(self, obj):
        obj = obj.workplace
        if not obj: return ''
        a, b = obj.split('/')
        workplace = get_workplace(f=True)
        return f'{workplace.get(a, {}).get("name")} / {workplace.get(a, {}).get("children", {}).get(b, {}).get("name")}'

    class Meta:
        model = UserModel
        fields = (
            'id',
            'get_full_name',
            'username',
            'email',
            'phone',
            'is_active',
            'department',
            'date_joined',
            'title',
            'workplace',
            'head_of_department',
            'work_management',
            'role',
        )


class UserSerializerU(rest.ModelSerializer):
    role = rest.IntegerField(source='role_id')

    class Meta:
        model = UserModel
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'is_active',
            'department',
            'title',
            'head_of_department',
            'work_management',
            'role',
        )


class UserSerializerC(rest.ModelSerializer):
    role = rest.IntegerField(source='role_id')

    def validate_username(self, attrs):
        if not re.match(r'^[A-Za-z0-9-_.]+$', attrs):
            raise rest.ValidationError('用户名不合法')
        return attrs

    def validate_phone(self, attrs):
        if not re.match(r'^1[34589]\d{9}$', attrs):
            raise rest.ValidationError('手机号码不合法')
        return attrs

    def validate_password(self, attrs):
        if not re.match(r'^\S{6,16}$', attrs):
            raise rest.ValidationError('密码不合法')
        return make_password(attrs)

    class Meta:
        model = UserModel
        read_only_fields = ('id',)
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'phone',
            'email',
            'department',
            'title',
            'is_active',
            'head_of_department',
            'work_management',
            'role',
        )


class UserView(rest.GenericViewSet, rest.ListModelMixin, rest.RetrieveModelMixin, rest.DestroyModelMixin, rest.UpdateModelMixin, rest.CreateModelMixin):
    queryset = UserModel.objects.all()
    pagination_class = rest.Pagination
    filter_backends = [rest.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']

    def list(self, request, *args, **kwargs):
        self.serializer_class = UserSerializerL
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = UserSerializerR
        response = super().retrieve(request, *args, **kwargs)
        serializer = serializers.serialize('json', DepartmentModel.objects.all(), fields=('name', 'id'))
        response.data.update({'department': [{'value': i['pk'], 'name': i['fields']['name']} for i in json.loads(serializer)]})
        return response

    def update(self, request, *args, **kwargs):
        self.serializer_class = UserSerializerU
        data = request.data
        if fullname := data.get('get_full_name'):
            last_name, first_name = fullname, ''
        else:
            last_name = first_name = ''
        if hasattr(data, '_mutable'): data._mutable = True
        request.data.update({'last_name': last_name, 'first_name': first_name})
        response = super().update(request, *args, **kwargs)
        if response.status_code == rest.HTTP_200_OK:
            if data.get('is_active') == 'false':
                UserModel.objects.filter(id__exact=kwargs.get('pk')).update(user_secret=uuid.uuid4())
            if data.get('head_of_department') == 'true':
                UserModel.objects.filter(
                    Q(department_id__exact=data.get('department')) & Q(head_of_department__exact=True) & ~Q(id__exact=kwargs.get('pk'))
                ).update(head_of_department=False, work_management=False)
        return response

    def create(self, request, *args, **kwargs):
        self.serializer_class = UserSerializerC
        data = request.data
        if self.queryset.filter(username__exact=data.get('username')): raise rest.ParseError(detail='用户名已存在')
        if fullname := data.get('get_full_name'):
            last_name, first_name = fullname, ''
        else:
            last_name = first_name = ''
        if hasattr(data, '_mutable'): data._mutable = True
        try:
            password = rsa_decrypt(data.get('password'))
        except (ValueError, AttributeError):
            raise rest.ParseError(detail='密码无法验证')
        request.data.update({'last_name': last_name, 'first_name': first_name, 'password': password})
        response = super().create(request, *args, **kwargs)
        if response.status_code == rest.HTTP_201_CREATED and data.get('head_of_department') == 'true':
            UserModel.objects.filter(
                Q(department_id__exact=data.get('department')) & Q(head_of_department__exact=True) & ~Q(id__exact=response.data['data'].get('id'))
            ).update(head_of_department=False, work_management=False)
        return response


class UserBatchSerializer(rest.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('is_active',)


class UserBatchView(rest.GenericViewSet, rest.UpdateModelMixin, rest.DestroyModelMixin):
    queryset = UserModel.objects.all()

    def verify(self):
        ids = list(set(self.kwargs.get('pk').split(',')))
        if '' in ids: ids.remove('')
        queryset = self.queryset.filter(id__in=ids)
        if len(ids) != queryset.count():
            raise rest.ParseError(detail='请求的数据包含了不能识别的数据')
        return queryset

    def update(self, request, *args, **kwargs):
        serializer = UserBatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = self.verify()
        queryset.update(is_active=serializer.data.get('is_active'))
        if serializer.initial_data.get('is_active') is False:
            queryset.update(user_secret=uuid.uuid4())
        return rest.Response()

    def destroy(self, request, *args, **kwargs):
        queryset = self.verify()
        queryset.delete()
        return rest.Response()


class DepartmentSerializer(rest.ModelSerializer):
    count = rest.SerializerMethodField()
    leader = rest.SerializerMethodField()
    work_management = rest.SerializerMethodField()
    leader_id = rest.SerializerMethodField()

    def get_leader_id(self, obj):
        if obj := obj.usermodel_set.filter(head_of_department__exact=True).first():
            return obj.id

    def get_count(self, obj):
        return obj.usermodel_set.count()

    def get_leader(self, obj):
        if obj := obj.usermodel_set.filter(head_of_department__exact=True):
            return obj.first().get_full_name()

    def get_work_management(self, obj):
        if obj := obj.usermodel_set.filter(work_management__exact=True):
            return obj.first().get_full_name()

    class Meta:
        model = DepartmentModel
        fields = ('id', 'name', 'count', 'leader', 'work_management', 'leader_id')


class DepartmentView(rest.GenericViewSet, rest.ListModelMixin, rest.DestroyModelMixin, rest.UpdateModelMixin, rest.CreateModelMixin):
    queryset = DepartmentModel.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = rest.Pagination
    filter_backends = [rest.SearchFilter]
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        name, leader = request.data.get('name'), request.data.get('leader')
        if not name: raise rest.ParseError(detail='名称字段是必须的')
        if self.queryset.filter(name__exact=name): raise rest.ParseError(detail='部门已存在')
        user = None
        if leader:
            if not str(leader).isdigit(): raise rest.ParseError(detail='部门负责人不合法')
            user = UserModel.objects.filter(id__exact=leader)
            if not user: raise rest.ParseError(detail='部门负责人不存在')
        obj = self.queryset.create(name=name)
        if user:
            user.update(department_id=obj.id, work_management=True, head_of_department=True)
        return rest.Response(status=rest.HTTP_201_CREATED, data={'name': name, 'leader': leader})


class RoleSerializer(rest.ModelSerializer):
    role = rest.SerializerMethodField(source='role')

    def get_role(self, obj):
        return json.loads(obj.role)

    class Meta:
        model = RoleModel
        fields = ('id', 'role', 'name', 'admin')
        read_only_fields = ('id', 'role', 'admin')


class RoleSerializerU(rest.ModelSerializer):
    class Meta:
        model = RoleModel
        fields = ('id', 'role', 'name', 'admin')
        read_only_fields = ('id', 'name', 'admin')


class RoleView(rest.GenericViewSet, rest.ListModelMixin, rest.UpdateModelMixin, rest.DestroyModelMixin, rest.CreateModelMixin):
    serializer_class = RoleSerializer
    queryset = RoleModel.objects.all()

    def list(self, request, *args, **kwargs):
        role = request.user.role_id
        response = super().list(request, *args, **kwargs)
        response.data['self'] = role
        return response

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not isinstance(request.data.get('role'), list): raise rest.ParseError(detail='规则参数格式错误')
        serializer = RoleSerializerU(instance, data={'role': format_role(request.data.get('role'))}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return rest.Response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        if self.queryset.filter(name__exact=request.data.get('name')): raise rest.ParseError(detail='角色名称已存在')
        return super().create(request, *args, **kwargs)
