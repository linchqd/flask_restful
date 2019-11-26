#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from resources.accounts.user import Users
from resources.accounts.login import Login


def add_resource(api):
    api.add_resource(Users, '/accounts/users/')
    api.add_resource(Login, '/accounts/login/')
