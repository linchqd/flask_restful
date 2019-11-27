#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource, reqparse, inputs, request, abort
from flask import g
from common.MaSchema import UserSchema, User, Group, Role, Permission


class Users(Resource):
    @staticmethod
    def get():
        name = request.args.get('name')
        if name:
            user = User.query.filter_by(name=name).first()
            if user:
                return UserSchema(exclude=('pwd_hash','access_token', 'token_expired')).dump(user)
            abort(404, message=u"user {} is not exist".format(name))
        return {"users": UserSchema(many=True, exclude=('pwd_hash','access_token', 'token_expired')).dump(User.query.all())}

    def post(self):
        parse = reqparse.RequestParser()
        data = self.add_arguments(parse).parse_args()
        errors = self.schema_validate(data)
        if errors:
            return errors
        for key in ['name', 'cname', 'phone_number', 'email']:
            res = self.verify_user_unique_fields({key: data[key]})
            if res:
                return {"message": res}
        user = User(**data)
        user.save()
        return {"user": {"id": user.id, "name": user.name}}

    def put(self):
        parse = reqparse.RequestParser()
        parse.add_argument('id', type=int, required=True, help=u'缺少参数id', location='json')
        data = self.add_arguments(parse).parse_args()
        errors = self.schema_validate(data)
        if errors:
            return errors
        user = User.query.get(data['id'])
        if user:
            res = self.update_items(user, data)
            if res:
                return res
            user.save()
            return {"user": user.name}
        abort(404, message="user is not exists")

    def patch(self):
        errors = self.schema_validate(request.json)
        if errors:
            return errors
        user = User.query.get(request.json.get("id"))
        if user:
            res = self.update_items(user, request.json)
            if res:
                return res
            user.save()
            return {"user": user.name}
        abort(404, message="user is not exists")

    @staticmethod
    def delete():
        user_id = request.json.get("id")
        user_list = []
        if isinstance(user_id, int):
            user_list.append(User.query.get(user_id))
        elif isinstance(user_id, list):
            user_list = User.query.filter(User.id.in_(user_id)).all()
        else:
            return {"message": "用户id必须为int or list类型"}
        if user_list:
            for u in user_list:
                u.delete()
            return {}
        abort(404, message="user is not exists")

    @staticmethod
    def schema_validate(data):
        errors = UserSchema(exclude=("groups", "roles", "permissions")).validate(data, partial=True)
        if errors:
            res = {"message": {}}
            for k, v in errors.items():
                res["message"][k] = ', '.join(v)
            return res
        return None

    @staticmethod
    def verify_user_unique_fields(data):
        if User.query.filter_by(**data).first():
            return "{} is existed".format(list(data.keys())[0])
        return None

    @staticmethod
    def add_arguments(parse):
        parse.add_argument('name', type=str, required=True, help=u'缺少用户名参数name', location='json')
        parse.add_argument('cname', type=str, required=True, help=u'缺少用户别名参数cname', location='json')
        parse.add_argument('is_super', type=inputs.boolean, default=False, location='json')
        parse.add_argument('status', type=inputs.boolean, default=True, location='json')
        parse.add_argument('phone_number', required=True, type=inputs.regex(r'1[3578]\d{9}'),
                           help=u'缺少phone_number参数或手机号码格式不对', location='json')
        parse.add_argument('email', type=str, required=True, help=u'缺少email参数或email格式不对', location='json')
        parse.add_argument('password', type=str, required=True, help=u"缺少密码参数password", location='json')
        return parse

    def update_items(self, user, data):
        for k, v in data.items():
            if hasattr(user, k) and getattr(user, k) != v:
                if k in ['name', 'cname', 'phone_number', 'email']:
                    res = self.verify_user_unique_fields({k: v})
                    if res:
                        return {"message": res}
                elif k in ['token_expired', 'ctime', 'login_time', 'last_time',
                           'access_token', 'is_super', 'pwd_hash'] and not g.user.is_super:
                    continue
                elif k == 'groups':
                    if not isinstance(v, list):
                        return {"message": "groups must be type of list"}
                    user.groups = Group.query.filter(Group.id.in_(v)).all()
                    continue
                elif k == 'roles':
                    if not isinstance(v, list):
                        return {"message": "roles must be type of list"}
                    user.roles = Role.query.filter(Role.id.in_(v)).all()
                    continue
                elif k == 'permissions':
                    if not isinstance(v, list):
                        return {"message": "permissions must be type of list"}
                    user.permissions = Permission.query.filter(Permission.id.in_(v)).all()
                    continue
                setattr(user, k, v)
        if data.get("password"):
            user.password = data.get("password")
        return None
