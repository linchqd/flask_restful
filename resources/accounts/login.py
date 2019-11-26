#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource, reqparse
from collections import defaultdict
import time
from resources.accounts.models import User

login_limit = defaultdict(int)


class Login(Resource):

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('username', type=str, required=True, help="username is required", location='json')
        self.parse.add_argument('password', type=str, required=True, help="password is required", location='json')
        super(Login, self).__init__()

    def post(self):
        args = self.parse.parse_args()
        user = User.query.filter_by(name=args.get('username')).first()
        if user:
            if user.status:
                if user.verify_password(args.get('password')):
                    login_limit.pop(user.name, None)
                    user.access_token = user.generate_auth_token()
                    user.token_expired = time.time() + 8 * 60 * 60
                    user.save()
                    return {
                        "username": user.name,
                        "nickname": user.cname,
                        "is_super": user.is_super,
                        "token": user.access_token,
                        "permissions": user.permissions
                    }
                else:
                    login_limit[user.name] += 1
                    if login_limit[user.name] >= 3:
                        user.update(status=False)
                    return {"mgs": "密码错误, 3次将被禁用, 当前次数: {}".format(login_limit[user.name])}
            else:
                return {"msg": "user {} is disabled!".format(user.name)}
        elif login_limit[args.get('username')] >=3:
            return {"msg": "user {} is disabled!".format(args.get('username'))}
        else:
            login_limit[args.get('username')] += 1
            return {"msg": "用户名不存在"}