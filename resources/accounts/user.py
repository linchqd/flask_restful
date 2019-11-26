#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource, reqparse, inputs
from common.MaSchema import UserSchema


class User(Resource):
    def get(self):
        us = UserSchema()
        data = {"email": "13435600095@163.com", "name": "fdfdfdfdfdf", "password": "134"}
        print(us.validate(data, partial=True))
        return {'task': 'pear'}, 200

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('name', type=str, required=True, help=u'缺少用户名参数: name')
        parse.add_argument('cname', type=str, required=True, help=u'')
        parse.add_argument('is_super', type=inputs.boolean)
        parse.add_argument('status', type=inputs.boolean)
        parse.add_argument('phone_number', required=True, type=inputs.regex(r'1[3578]\d{9}'), help=u'')
        parse.add_argument('email', type=str, required=True, help=u'')
        data = parse.parse_args()
        print(data)