#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from app import app, api
from config import HOST, DEBUG, PORT
from resources import accounts


accounts.add_resource(api)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)