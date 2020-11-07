#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import html

from lib import m_rest_framework as rest
from .models import RepositoryModel


class RepositorySerializer(rest.ModelSerializer):
    author_name = rest.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = RepositoryModel
        fields = ('id', 'title', 'content', 'update', 'author', 'author_name')
        read_only_fields = ('id', 'update')


class RepositorySerializerU(rest.ModelSerializer):
    class Meta:
        model = RepositoryModel
        fields = ('title', 'content')

    def validate_content(self, val):
        if val: return html.escape(val)
        return val

    def validate_title(self, val):
        if val: return html.escape(val)
        return val


class RepositoryView(rest.GenericViewSet, rest.ListModelMixin, rest.CreateModelMixin):
    queryset = RepositoryModel.objects.all()
    serializer_class = RepositorySerializer
    filter_backends = [rest.SearchFilter]
    pagination_class = rest.Pagination
    search_fields = ['title', 'author__first_name', 'author__last_name']

    def get_queryset(self):
        return self.queryset.filter(draft__exact=False)

    def create(self, request, *args, **kwargs):
        data = dict(
            title=html.escape(request.data.get('title', '')),
            content=html.escape(request.data.get('content', '')),
            author=request.user.id,
        )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return rest.Response(data=serializer.data, status=rest.HTTP_201_CREATED, headers=headers)


class MyRepositoryView(rest.GenericViewSet, rest.ListModelMixin, rest.UpdateModelMixin, rest.DestroyModelMixin, rest.RetrieveModelMixin):
    queryset = RepositoryModel.objects.all()
    serializer_class = RepositorySerializer
    filter_backends = [rest.SearchFilter]
    pagination_class = rest.Pagination
    search_fields = ['title', 'author__first_name', 'author__last_name']

    def get_queryset(self):
        return self.queryset.filter(author__exact=self.request.user, draft__exact=False)

    def update(self, request, *args, **kwargs):
        self.serializer_class = RepositorySerializerU
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == rest.HTTP_200_OK:
            response.data['data']['content'] = html.unescape(response.data['data']['content'])
        return response


class DraftSerializer(rest.ModelSerializer):
    class Meta:
        model = RepositoryModel
        fields = ('id', 'title', 'content', 'update')
        read_only_fields = ('id', 'update')

    def validate_content(self, val):
        if val: return html.escape(val)
        return val

    def validate_title(self, val):
        if val: return html.escape(val)
        return val


class DraftSerializerC(rest.ModelSerializer):
    class Meta:
        model = RepositoryModel
        fields = ('id', 'title', 'content', 'update', 'draft', 'author')
        read_only_fields = ('id', 'update')

    def validate_content(self, val):
        if val: return html.escape(val)
        return val

    def validate_title(self, val):
        if val: return html.escape(val)
        return val


class DraftSerializerU(rest.ModelSerializer):
    class Meta:
        model = RepositoryModel
        fields = ('id', 'title', 'content', 'update', 'draft')
        read_only_fields = ('id', 'update')

    def validate_content(self, val):
        if val: return html.escape(val)
        return val

    def validate_title(self, val):
        if val: return html.escape(val)
        return val


class DraftView(rest.GenericViewSet, rest.ListModelMixin, rest.UpdateModelMixin, rest.CreateModelMixin, rest.DestroyModelMixin, rest.RetrieveModelMixin):
    queryset = RepositoryModel.objects.filter(draft__exact=True)
    serializer_class = DraftSerializer

    def get_queryset(self):
        return self.queryset.filter(author_id__exact=self.request.user.id)

    def create(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'draft': True,
            'author': request.user.id,
        }
        serializer = DraftSerializerC(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return rest.Response(data=serializer.data, status=rest.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        self.serializer_class = DraftSerializerU
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == rest.HTTP_200_OK:
            response.data['data']['content'] = html.unescape(response.data['data']['content'])
        return response
