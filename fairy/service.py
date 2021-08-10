'''
Author : hupeng
Time : 2021/8/6 14:47 
Description: 
'''
import json
import traceback

from flask import request

from fairy.const import Code
from fairy.utils.log import error_log
from fairy.utils.response import MyResponse


class BaseConfig(object):
    def __init__(self):
        self.data = {}

    def dumps(self):
        return json.dumps(self.data)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)


class BaseService(object):
    config = None
    params_class = None
    __is_init = False

    @classmethod
    def init(cls, cfg: dict):
        print('init...')
        cls.error_log = cfg.get('log_dir', error_log('./log'))
        cls.CODE_SUCCESS = cfg.get('CODE_SUCCESS', Code(0, '成功'))
        cls.CODE_PARAM = cfg.get('CODE_PARAM', Code(10000, '参数错误'))
        cls.CODE_SERVICE = cfg.get('CODE_SERVICE', Code(10001, '服务异常'))
        cls.__is_init = True

    def __init__(self):
        self._request = request
        self.params = None

    def get_params(self):
        if self.params_class is None:
            return
        params = self.params_class.build()
        self.params = params
        return params

    def prints(self, text: str, p=True, c=False):
        if p and c:
            print('\033[0;32m{}\033[0m'.format(text))
        elif p:
            print(text)

    def make_response(self) -> MyResponse:
        response = MyResponse()
        # 参数校验
        try:
            if not self.__is_init:
                self.init({})
            self.get_params()
        except Exception as e:
            response.code = self.CODE_PARAM.val
            response.message = str(e)
            self.error_log.write('got a params error %s' %
                            str(traceback.format_exc()))
            return response

        response.code = self.CODE_SUCCESS.val
        response.message = self.CODE_SUCCESS.msg
        try:
            response = self.get_response(response)
        except Exception as e:
            response.code = self.CODE_SERVICE.val
            response.message = f'{self.CODE_SERVICE.msg}: {str(e)}'
            self.error_log.write(str(traceback.format_exc()))
        return response

    def get_response(self, response: MyResponse) -> MyResponse:
        raise NotImplementedError()
