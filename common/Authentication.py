#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from flask import g
from functools import wraps


def permission_required(permission):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not g.user.is_super:
                permission_list = [x.strip() for x in permission.split('|')]
                for p in permission_list:
                    req_permission_set = {x for x in p.split('&')}
                    if req_permission_set.issubset(g.user.get_permissions()):
                        break
                else:
                    return {"message": "Permission denied"}, 403
            return func(*args, **kwargs)
        return wrapper
    return decorate
