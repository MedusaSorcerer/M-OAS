#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import json

from rest_framework import permissions


def _(permission, method):
    if permission == '__all__':
        return True
    if isinstance(permission, list):
        return method in permission
    return False


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        >>> {'numberSign_1': '__all__', 'numberSign_2': ['list', 'update', 'create', 'destroy', 'retrieve']}
        """
        try:
            method = request.parser_context['view'].action
        except AttributeError:
            method = {'GET': 'list', 'POST': 'create', 'DELETE': 'destroy', 'PUT': 'update'}.get(request.method)
        if hasattr(view, 'permission'):
            role_obj = request.user.role
            if not role_obj: return False
            permission, role = view.permission, json.loads(role_obj.role)
            for i1 in role:
                if children := i1.get('children'):
                    for i2 in children:
                        if i2['id'] in permission and all([i2['spread'], i1['spread']]) and _(permission[i2['id']], method):
                            break
                    else:
                        continue
                    break
                else:
                    if i1['id'] in permission and i1['spread'] is True and _(permission[i1['id']], method):
                        break
            else:
                return False
        return bool(request.user and request.user.is_authenticated)
