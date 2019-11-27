#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
from marshmallow import EXCLUDE, fields

from app import ma
from resources.accounts.models import User, Group, Role, Permission


class PermissionSchema(ma.ModelSchema):

    class Meta:
        model = Permission
        unknown = EXCLUDE


class RoleSchema(ma.ModelSchema):
    permissions = fields.Nested(PermissionSchema, many=True, only=('id', 'name', 'desc', 'ctime'))

    class Meta:
        model = Role
        unknown = EXCLUDE


class GroupSchema(ma.ModelSchema):
    roles = fields.Nested(RoleSchema, many=True, only=('id', 'name', 'desc', 'ctime'))
    permissions = fields.Nested(PermissionSchema, many=True, only=('id', 'name', 'desc', 'ctime'))

    class Meta:
        model = Group
        unknown = EXCLUDE


class UserSchema(ma.ModelSchema):
    email = fields.Email(required=True, validate=[lambda n: len(n) <= 32])
    groups = fields.Nested(GroupSchema, many=True, only=('id', 'name', 'desc', 'ctime'))
    roles = fields.Nested(RoleSchema, many=True, only=('id', 'name', 'desc', 'ctime'))
    permissions = fields.Nested(PermissionSchema, many=True, only=('id', 'name', 'desc', 'ctime'))

    class Meta:
        model = User
        unknown = EXCLUDE
