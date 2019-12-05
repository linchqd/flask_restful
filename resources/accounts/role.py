#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource, reqparse, request, abort
from flask import g

from resources.accounts.models import Role
from common.MaSchema import RoleSchema, UserSchema, GroupSchema, User, Group, Permission
from common.Authentication import permission_required


class Roles(Resource):
    @permission_required('role_get_list')
    def get(self):
        name = request.args.get("name")
        if name:
            role = Role.query.filter_by(name=name).first()
            if role:
                return {"data": self.dump_user_and_group(RoleSchema().dump(role))}
            abort(404, message="role is not exists")
        return {"data": self.dump_user_and_group(RoleSchema(many=True).dump(Role.query.all()))}

    @permission_required('role_add')
    def post(self):
        data = self.add_arguments()
        errors = self.schema_validate(data)
        if errors:
            return errors
        for key in ['name', 'desc']:
            res = self.verify_role_unique_fields({key: data[key]})
            if res:
                return {"message": res}
        role = Role(**data)
        role.save()
        return {"data": "添加成功"}

    @permission_required('role_update')
    def put(self):
        data = self.add_arguments(put=True)
        errors = self.schema_validate(data)
        if errors:
            return errors
        role = Role.query.get(data.get("id"))
        if role:
            res = self.update_items(role, data)
            if res:
                return res
            role.save()
            return {"data": "更新成功"}
        abort(404, message="role is not exists")

    @permission_required('role_modify')
    def patch(self):
        errors = self.schema_validate(request.json)
        if errors:
            return errors
        role = Role.query.get(request.json.get("id"))
        if role:
            res = self.update_items(role, request.json)
            if res:
                return res
            role.save()
            return {"data": "修改成功"}
        abort(404, message="role is not exists")

    @staticmethod
    @permission_required('role_delete')
    def delete():
        role_id = request.json.get("id")
        role_list = []
        if isinstance(role_id, int):
            role_list.append(Role.query.get(role_id))
        elif isinstance(role_id, list):
            role_list = Role.query.filter(Role.id.in_(role_id)).all()
        else:
            return {"message": "角色id必须为int or list类型"}
        if role_list:
            for role in role_list:
                role.delete()
            return {'data': '删除成功'}
        abort(404, message="role is not exists")

    @staticmethod
    def dump_user_and_group(roles):
        if isinstance(roles, list):
            for role in roles:
                role['users'] = UserSchema(
                    many=True,
                    only=("id", "name", "cname", "phone_number", "email")
                ).dump(User.query.filter(User.id.in_(role['users'])).all())
                role['groups'] = GroupSchema(
                    many=True,
                    only=('id', 'name', 'desc', 'ctime')
                ).dump(Group.query.filter(Group.id.in_(role['groups'])).all())

        else:
            roles['users'] = UserSchema(
                many=True,
                only=("id", "name", "cname", "phone_number", "email")
            ).dump(User.query.filter(User.id.in_(roles['users'])).all())
            roles['groups'] = GroupSchema(
                many=True,
                only=('id', 'name', 'desc', 'ctime')
            ).dump(Group.query.filter(Group.id.in_(roles['groups'])).all())
        return roles

    @staticmethod
    def add_arguments(put=False):
        parse = reqparse.RequestParser()
        parse.add_argument('name', type=str, required=True, help=u'role name is required', location='json')
        parse.add_argument('desc', type=str, required=True, help=u'role desc is required', location='json')
        if put:
            parse.add_argument('id', type=int, required=True, help=u'role id is required', location='json')
        return parse.parse_args()

    @staticmethod
    def schema_validate(data):
        errors = RoleSchema(exclude=("users", "groups", "permissions")).validate(data, partial=True)
        if errors:
            res = {"message": {}}
            for k, v in errors.items():
                res["message"][k] = ', '.join(v)
            return res
        return None

    @staticmethod
    def verify_role_unique_fields(data):
        if Role.query.filter_by(**data).first():
            return "{} is existed".format(list(data.keys())[0])
        return None

    def update_items(self, obj, data):
        for k, v in data.items():
            if hasattr(obj, k) and getattr(obj, k) != v:
                if k in ['name', 'desc']:
                    res = self.verify_role_unique_fields({k: v})
                    if res:
                        return {"message": res}
                elif k == 'users':
                    if not isinstance(v, list):
                        return {"message": "users must be type of list"}
                    obj.users = User.query.filter(User.id.in_(v)).all()
                    continue
                elif k == 'groups':
                    if not isinstance(v, list):
                        return {"message": "groups must be type of list"}
                    obj.groups = Group.query.filter(Group.id.in_(v)).all()
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
