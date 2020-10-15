#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from lib import m_rest_framework as rest
from .models import RepositoryModel


def summary(content):
    return content


class RepositorySerializer(rest.ModelSerializer):
    author_name = rest.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = RepositoryModel
        fields = ('id', 'title', 'content', 'update', 'author', 'author_name')
        read_only_fields = ('id', 'update')


class RepositoryView(rest.GenericViewSet, rest.ListModelMixin, rest.CreateModelMixin):
    queryset = RepositoryModel.objects.all()
    serializer_class = RepositorySerializer
    filter_backends = [rest.SearchFilter]
    pagination_class = rest.Pagination
    search_fields = ['title', 'author__first_name', 'author__last_name']

    def create(self, request, *args, **kwargs):
        data = dict(
            title=request.data.get('title'),
            content=request.data.get('content'),
            author=request.user.id,
        )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return rest.Response(data=serializer.data, status=rest.HTTP_201_CREATED, headers=headers)
