#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from flask import request, make_response


def init_app(app):
    app.before_request(cross_domain_access_before)
    app.before_request(login_verify)
    app.after_request(cross_domain_access_after)


def login_verify():
    token = request.headers.get('X-TOKEN')
    if request.path == '/login':
        return None
    return {"msg": "Auth fail, please login"}, 401


def cross_domain_access_before():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'X-TOKEN'
        response.headers['Access-Control-Max-Age'] = 24 * 60 * 60
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE', 'OPTIONS'
        return response


def cross_domain_access_after(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-TOKEN'
    return response
