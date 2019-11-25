#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource, reqparse
from resources.accounts.models import User


class Login(Resource):

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('username', type=str, required=True, help="username is required", location='json')
        self.parse.add_argument('password', type=str, required=True, help="password is required", location='json')
        super(Login, self).__init__()

    def post(self):
        args = self.parse.parse_args()
        user = User.query.filter_by(name=args.get('username')).first()
        print(user)
        if user and user.verify_password(args.get('password')):
            return {"msg": "login successful!"}
        return {"msg": "Auth fail!"}
