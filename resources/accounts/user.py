#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource, reqparse, inputs, request
from common.MaSchema import UserSchema, User


class Users(Resource):
    @staticmethod
    def get():
        name = request.args.get('name')
        if name:
            user = User.query.filter_by(name=name).first()
            if user:
                return UserSchema(exclude=('pwd_hash','access_token', 'token_expired')).dump(user)
            return {"message": "user {} is not exist".format(name)}
        return {"users": UserSchema(many=True, exclude=('pwd_hash','access_token', 'token_expired')).dump(User.query.all())}

    def post(self):
        parse = reqparse.RequestParser()
        data = self.add_arguments(parse).parse_args()
        errors = UserSchema().validate(data, partial=True)
        if errors:
            res = {"message": {}}
            for k, v in errors.items():
                res["message"][k] = ', '.join(v)
            return res
        for key in ['name', 'cname', 'phone_number', 'email']:
            res = self.verify_user_unique_fields({key: data[key]})
            if res:
                return {"message": res}
        user = User(**data)
        user.save()
        return {"user": user.name}

    def put(self):
        parse = reqparse.RequestParser()
        parse.add_argument('id', type=int, required=True, help=u'缺少参数id', location='json')
        data = self.add_arguments(parse).parse_args()
        errors = UserSchema().validate(data, partial=True)
        if errors:
            res = {"message": []}
            for k, v in errors.items():
                res["message"].append({k: ', '.join(v)})
            return res
        user = User.query.get(data['id'])
        if user:
            for k, v in data.items():
                if hasattr(user, k) and getattr(user, k) != v:
                    if k in ['name', 'cname', 'phone_number', 'email']:
                        res = self.verify_user_unique_fields({k: v})
                        if res:
                            return {"message": res}
                    setattr(user, k, v)
            user.save()
            return {"user": user.name}
        return {"message": "用户不存在"}

    def patch(self):
        user_id = request.json.get("id")
        if not isinstance(user_id, int):
            return {"message": "user id must be of int type"}
        user = User.query.get(user_id)
        if not user:
            return {"message": "user is not exists"}
        for k, v in request.json.items():
            if hasattr(user, k) and getattr(user, k) != v:
                if k in ['name', 'cname', 'phone_number', 'email']:
                    res = self.verify_user_unique_fields({k: v})
                    if res:
                        return {"message": res}

                setattr(user, k, v)


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
        return {"message": "用户不存在"}

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

