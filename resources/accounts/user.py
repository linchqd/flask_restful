#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from flask_restful import Resource


class User(Resource):
    def get(self):
        return {'task': 'pear'}, 200

