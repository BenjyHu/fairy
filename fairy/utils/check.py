'''
Author : hupeng
Time : 2021/8/6 14:57 
Description: 
'''
from flask import request, g
from pydantic import BaseModel


class Params(BaseModel):
    requestid: str = None

    @classmethod
    def params(cls):
        args = request.json
        if args is None:
            try:
                args = request.form.to_dict()
            except:
                args = {}
        return args

    @classmethod
    def build(cls):
        params = cls(**cls.params())
        params.requestid = g.requestid
        return params
