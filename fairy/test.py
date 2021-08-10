'''
Author : hupeng
Time : 2021/8/9 15:24 
Description: 
''' 
from fairy import BaseService
from fairy.utils import MyResponse, responser

class Service(BaseService):
    def get_response(self, response: MyResponse):
        return response

from flask import Flask

app = Flask(__name__)


@app.route('/')
def f():
    s = Service()
    res = s.make_response()
    return responser(res)


if __name__ == '__main__':
    app.run()
