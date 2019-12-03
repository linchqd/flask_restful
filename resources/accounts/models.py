#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from app import db
from common.sqlmixins import SqlMixin


class Permission(db.Model, SqlMixin):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False, unique=True)
    desc = db.Column(db.String(255), nullable=False)
    ctime = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Permission {}: {}>'.format(self.id, self.name)

    class Meta:
        ordering = ('-id',)


class Role(db.Model, SqlMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(32), unique=True, nullable=False)
    desc = db.Column(db.String(255), nullable=False)
    ctime = db.Column(db.DateTime, default=datetime.now)
    permissions = db.relationship('Permission', secondary='role_permission', backref=db.backref('roles', lazy='dynamic'))

    def __repr__(self):
        return '<Role {}: {}>'.format(self.id, self.name)

    class Meta:
        ordering = ('-id',)


class User(db.Model, SqlMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(16), unique=True, nullable=False)
    cname = db.Column(db.String(16), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(100), nullable=False)
    is_super = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=True)
    phone_number = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    access_token = db.Column(db.String(32))
    token_expired = db.Column(db.Integer)
    ctime = db.Column(db.DateTime, default=datetime.now)
    login_time = db.Column(db.DateTime, default=datetime.now)
    last_time = db.Column(db.DateTime, default=datetime.now)
    groups = db.relationship('Group', secondary='user_group', backref=db.backref('users', lazy='dynamic'))
    roles = db.relationship('Role', secondary='user_role', backref=db.backref('users', lazy='dynamic'))
    permissions = db.relationship('Permission', secondary='user_permission', backref=db.backref('users', lazy='dynamic'))

    @property
    def password(self):
        raise AttributeError('密码为私有属性，不允许访问')

    @password.setter
    def password(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)

    @staticmethod
    def generate_auth_token():
        return uuid.uuid4().hex

    @staticmethod
    def permission_join(p_set, p_obj_list):
        for p_obj in p_obj_list:
            p_set.add(p_obj.name)
        return p_set

    def get_permissions(self):
        permission_set = set()
        if self.is_super:
            return set()
        if self.permissions:
            permission_set = self.permission_join(permission_set, self.permissions)
        if self.groups:
            for group in self.groups:
                if group.permissions:
                    permission_set = self.permission_join(permission_set, group.permissions)
        if self.roles:
            for role in self.roles:
                if role.permissions:
                    permission_set = self.permission_join(permission_set, role.permissions)
        return permission_set

    def __repr__(self):
        return '<User {}: {}>'.format(self.id, self.name)

    class Meta:
        ordering = ('-id',)


class Group(db.Model, SqlMixin):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(16), unique=True, nullable=False)
    desc = db.Column(db.String(255), nullable=False)
    ctime = db.Column(db.DateTime, default=datetime.now)
    roles = db.relationship('Role', secondary='group_role', backref=db.backref('groups', lazy='dynamic'))
    permissions = db.relationship('Permission', secondary='group_permission', backref=db.backref('groups', lazy='dynamic'))

    def __repr__(self):
        return '<Group {}: {}>'.format(self.id, self.name)

    class Meta:
        ordering = ('-id',)


# 权限与角色关联表
role_permission = db.Table('role_permission', db.Column('role_id', db.Integer, db.ForeignKey('roles.id')), db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id')))

# 用户与用户组关联表
user_group = db.Table('user_group', db.Column('user_id', db.Integer, db.ForeignKey('users.id')), db.Column('group_id', db.Integer, db.ForeignKey('groups.id')))

# 用户与角色关联表
user_role = db.Table('user_role', db.Column('user_id', db.Integer, db.ForeignKey('users.id')), db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))

# 用户与权限关联表
user_permission = db.Table('user_permission', db.Column('user_id', db.Integer, db.ForeignKey('users.id')), db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id')))

# 用户组与角色关联表
group_role = db.Table('group_role', db.Column('group_id', db.Integer, db.ForeignKey('groups.id')), db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))

# 用户组与权限关联表
group_permission = db.Table('group_permission', db.Column('group_id', db.Integer, db.ForeignKey('groups.id')), db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id')))

