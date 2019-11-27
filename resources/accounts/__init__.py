#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from resources.accounts.user import Users
from resources.accounts.group import Groups
from resources.accounts.login import Login
from resources.accounts.role import Roles
from resources.accounts.permission import Permissions


def add_resource(api):
    api.add_resource(Users, '/accounts/users/')
    api.add_resource(Groups, '/accounts/groups/')
    api.add_resource(Roles, '/accounts/roles/')
    api.add_resource(Permissions, '/accounts/permissions/')
    api.add_resource(Login, '/accounts/login/')
