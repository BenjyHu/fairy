'''
Author : hupeng
Time : 2021/8/6 14:49 
Description: 
'''
import json

from flask import Response


class MyResponse(object):

    def __init__(self, code: int = None, message: str = None, data: dict = None):
        self.code = code or None
        self.message = message or ''
        self.data = data or {}

    @property
    def dict(self):
        return self.__dict__

    def dumps(self):
        return json.dumps(self.dict)


def responser(response: MyResponse = None, *, code=0, data=None, message='') -> Response:
    if response is None:
        response = MyResponse()
        response.code = code
        response.message = str(message)
        response.data = data
    return Response(
        response=json.dumps(response.dict, ensure_ascii=False),
        mimetype='application/json',
    )
