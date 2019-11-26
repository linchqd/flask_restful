#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from flask import request, make_response, g
import time
from resources.accounts.models import User


def init_app(app):
    app.before_request(cross_domain_access_before)
    app.before_request(login_verify)
    app.after_request(cross_domain_access_after)


def login_verify():
    if request.path == '/accounts/login/':
        return None
    token = request.headers.get('X-TOKEN')
    if token and len(token) == 32:
        g.user = User.query.filter_by(access_token=token).first()
        if g.user and g.user.status and g.user.token_expired >= time.time():
            g.user.token_expired = time.time() + 8 * 60 * 60
            g.user.save()
            return None
    return {"message": "Auth fail, please login"}, 401


def cross_domain_access_before():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'X-TOKEN'
        response.headers['Access-Control-Max-Age'] = 8 * 60 * 60
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE', 'OPTIONS'
        return response


def cross_domain_access_after(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-TOKEN'
    return response
