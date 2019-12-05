#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource, reqparse, request, abort
from flask import g

from resources.accounts.models import Group
from common.MaSchema import GroupSchema, UserSchema, User, Role, Permission
from common.Authentication import permission_required


class Groups(Resource):
    @permission_required('group_get_list')
    def get(self):
        name = request.args.get("name")
        if name:
            group = Group.query.filter_by(name=name).first()
            if group:
                return {"data": self.dump_user(GroupSchema().dump(group))}
            abort(404, message="group is not exists")
        return {"data": self.dump_user(GroupSchema(many=True).dump(Group.query.all()))}

    @permission_required('group_add')
    def post(self):
        data = self.add_arguments()
        errors = self.schema_validate(data)
        if errors:
            return errors
        for key in ['name', 'desc']:
            res = self.verify_group_unique_fields({key: data[key]})
            if res:
                return {"message": res}
        group = Group(**data)
        group.save()
        return {"data": "添加成功"}

    @permission_required('group_update')
    def put(self):
        data = self.add_arguments(put=True)
        errors = self.schema_validate(data)
        if errors:
            return errors
        group = Group.query.get(data.get("id"))
        if group:
            res = self.update_items(group, data)
            if res:
                return res
            group.save()
            return {"data": '更新成功'}
        abort(404, message="group is not exists")

    @permission_required('group_modify')
    def patch(self):
        errors = self.schema_validate(request.json)
        if errors:
            return errors
        group = Group.query.get(request.json.get("id"))
        if group:
            res = self.update_items(group, request.json)
            if res:
                return res
            group.save()
            return {"data": '修改成功'}
        abort(404, message="group is not exists")

    @staticmethod
    @permission_required('group_delete')
    def delete():
        group_id = request.json.get("id")
        group_list = []
        if isinstance(group_id, int):
            group_list.append(Group.query.get(group_id))
        elif isinstance(group_id, list):
            group_list = Group.query.filter(Group.id.in_(group_id)).all()
        else:
            return {"message": "用户组id必须为int or list类型"}
        if group_list:
            for group in group_list:
                group.delete()
            return {"data": "删除成功"}
        abort(404, message="group is not exists")

    def update_items(self, obj, data):
        for k, v in data.items():
            if hasattr(obj, k) and getattr(obj, k) != v:
                if k in ['name', 'desc']:
                    res = self.verify_group_unique_fields({k: v})
                    if res:
                        return {"message": res}
                elif k == 'users':
                    if not isinstance(v, list):
                        return {"message": "users must be type of list"}
                    obj.users = User.query.filter(User.id.in_(v)).all()
                    continue
                elif k == 'roles':
                    if not isinstance(v, list):
                        return {"message": "roles must be type of list"}
                    obj.roles = Role.query.filter(Role.id.in_(v)).all()
                    continue
                elif k == 'permissions':
                    if not isinstance(v, list):
                        return {"message": "permissions must be type of list"}
                    if not g.user.is_super:
                        return {"message": "Permission denied"}, 403
                    obj.permissions = Permission.query.filter(Permission.id.in_(v)).all()
                    continue
                setattr(obj, k, v)
        return None

    @staticmethod
    def verify_group_unique_fields(data):
        if Group.query.filter_by(**data).first():
            return "{} is existed".format(list(data.keys())[0])
        return None

    @staticmethod
    def dump_user(groups):
        if isinstance(groups, list):
            for group in groups:
                if group['users']:
                    group['users'] = UserSchema(
                        many=True,
                        only=("id", "name", "cname", "phone_number", "email")
                    ).dump(User.query.filter(User.id.in_(group['users'])).all())
        else:
            if groups['users']:
                groups['users'] = UserSchema(
                    many=True,
                    only=("id", "name", "cname", "phone_number", "email")
                ).dump(User.query.filter(User.id.in_(groups['users'])).all())
        return groups

    @staticmethod
    def add_arguments(put=False):
        parse = reqparse.RequestParser()
        parse.add_argument('name', type=str, required=True, help=u'group name is required', location='json')
        parse.add_argument('desc', type=str, required=True, help=u'group desc is required', location='json')
        if put:
            parse.add_argument('id', type=int, required=True, help=u'group id is required', location='json')
        return parse.parse_args()

    @staticmethod
    def schema_validate(data):
        errors = GroupSchema(exclude=("users", "roles", "permissions")).validate(data, partial=True)
        if errors:
            res = {"message": {}}
            for k, v in errors.items():
                res["message"][k] = ', '.join(v)
            return res
        return None
