#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
from marshmallow import EXCLUDE, fields

from app import ma
from resources.accounts.models import User, Group, Role, Permission


class UserSchema(ma.ModelSchema):
    email = fields.Email(required=True, validate=[lambda n: len(n) <= 32])

    class Meta:
        model = User
        unknown = EXCLUDE
