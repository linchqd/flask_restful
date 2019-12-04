#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import os, sys, datetime
from functools import wraps
from getpass import getpass
from resources.accounts.models import User


func_name = {}
func_desc = {}


def command(command_name, command_desc):
    def decorate(func):
        func_name[command_name] = func
        func_desc[command_name] = command_desc
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorate


def input_password(pwd):
    if pwd.strip():
        pwd2 = getpass("请再次输入密码")
        if pwd2.strip() == pwd:
            return pwd
        else:
            return input_password(getpass('两次输入密码不一致，请重新输入管理员账户密码: '))
    else:
        return input_password(getpass('密码不能为空，请输入管理员账户密码: '))


@command('init_db', "初始化数据库")
def init_db():
    from app import db
    from resources.accounts import models
    user_input = input('是否要初始化数据库，该操作会清空所有数据[y|n]？')
    if user_input.strip() == 'y':
        db.drop_all()
        db.create_all()
        sql = os.path.join(os.path.dirname(os.path.abspath(__file__)), "common", "sql", "init.sql")
        with open(sql, 'r') as f:
            line = f.readline()
            while line:
                if line.startswith("INSERT INTO"):
                    db.engine.execute(line.strip().format(datetime.datetime.now()))
                line = f.readline()
        print('数据库已初始化成功! 管理员账号: admin 管理员密码: admin')


@command('reset_pwd', "重置管理员密码")
def reset_pwd():
    username = input("请输入管理员用户名: ")
    user = User.query.filter_by(name=username).first()
    if user:
        password = input_password(getpass("请输入密码: "))
        user.password = password
        user.save()
        print("重置密码成功!")
    else:
        print("管理员不存在,请确认!")
        return reset_pwd()


help_info = """
usage: {} <command>
command:
"""

for k, v in func_desc.items():
    help_info += "\t{} \t{}\n".format(k, v)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(help_info.format(sys.argv[0]))
        sys.exit(1)
    fun_name = func_name.get(sys.argv[1])
    if fun_name and callable(fun_name):
        fun_name()
    else:
        print(help_info.format(sys.argv[0]))


