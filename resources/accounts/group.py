#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource, reqparse, request

from resources.accounts.models import Group
from common.MaSchema import GroupSchema, UserSchema, User


class Groups(Resource):
    def get(self):
        name = request.args.get("name")
        if name:
            group = Group.query.filter_by(name=name).first()
            if group:
                return {"group": self.dump_user(GroupSchema().dump(group))}
        return {"groups": self.dump_user(GroupSchema(many=True).dump(Group.query.all()))}

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
        return {"group": {"id": group.id, "name": group.name}}

    def put(self):
        pass

    def patch(self):
        pass

    @staticmethod
    def delete():
        group_id = request.json.get("id")
        group_list = []
        if isinstance(group_id, int):
            group_list.append(Group.query.get(group_id))
        elif isinstance(group_id, list):
            user_list = User.query.filter(Group.id.in_(group_id)).all()
        else:
            return {"message": "用户组id必须为int or list类型"}
        if group_list:
            for group in group_list:
                group.delete()
            return {}
        return {"message": "用户组不存在"}

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
    def add_arguments():
        parse = reqparse.RequestParser()
        parse.add_argument('name', type=str, required=True, help=u'group name is required', location='json')
        parse.add_argument('desc', type=str, required=True, help=u'group desc is required', location='json')
        return parse.parse_args()

    @staticmethod
    def schema_validate(data):
        errors = GroupSchema(exclude=("roles", "permissions")).validate(data, partial=True)
        if errors:
            res = {"message": {}}
            for k, v in errors.items():
                res["message"][k] = ', '.join(v)
            return res
        return None
