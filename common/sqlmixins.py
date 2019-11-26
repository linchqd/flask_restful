#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


from app import db


def commit():
    try:
        db.session.commit()
    except Exception as E:
        db.session.rollback()
        raise


class SqlMixin(object):
    __slots__ = ()

    def add(self):
        db.session.add(self)

    def update(self, **kwargs):
        is_change = False
        for k, v in kwargs.items():
            if hasattr(self, k) and getattr(self, k) != v:
                is_change = True
                setattr(self, k, v)
        if is_change:
            commit()
        return is_change

    def save(self):
        db.session.add(self)
        commit()
        return self

    def delete(self):
        db.session.delete(self)
        commit()

