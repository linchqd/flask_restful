#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource, request, abort
from common.MaSchema import PermissionSchema, Permission
from common.Authentication import permission_required


class Permissions(Resource):
    @staticmethod
    @permission_required('permission_get_list')
    def get():
        pid = request.args.get("id")
        if pid:
            permission = Permission.query.get(pid)
            if permission:
                return {"data": PermissionSchema().dump(permission)}
            else:
                abort(404, message=u'permission is not exist')
        return {"data": PermissionSchema(many=True).dump(Permission.query.all())}
