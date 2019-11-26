#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from resources.accounts.user import User
from resources.accounts.login import Login


def add_resource(api):
    api.add_resource(User, '/')
    api.add_resource(Login, '/accounts/login')
