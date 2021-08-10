'''
Author : hupeng
Time : 2021/1/12 10:55 
Description: 
'''
import os
import json
import logging
from functools import partial
from logging.handlers import TimedRotatingFileHandler

import flask
from flask import g


class RequestId():
    def __init__(self):
        self.requestid = None


rd = RequestId()


class Record():
    def __init__(self):
        self.d = {}

    def reset(self):
        self.d.clear()

    def is_empty(self):
        return False if self.d else True

    def dumps(self):
        return json.dumps(self.d)

    def __setitem__(self, key, value):
        self.d[key] = value

    def __getitem__(self, item):
        return self.d[item]

    def __str__(self):
        return str(self.d)

    def __repr__(self):
        return str(self.d)


processing = Record()
time_record = Record()
statistics_record = Record()


class Formatter(logging.Formatter):
    def format(self, record):
        if flask.globals._request_ctx_stack.top is not None:
            record.requestid = g.requestid
        else:
            record.requestid = rd.requestid
        result = super(Formatter, self).format(record)
        return result


class MyLogging():

    def __init__(self, log_dir, log_name='', file_name='error'):
        self.logger = logging.getLogger(log_name)
        self.base_dir = log_dir
        self.check_root_dir()
        self.set_log_level(file_name)
        self.formatter = Formatter(
            f'[%(asctime)s] |%(levelname)s|[line:%(lineno)d][requestid:%(requestid)s] %(message)s')
        filename = os.path.join(self.base_dir, '{}_{}.log'.format(file_name, os.getpid()))
        file_handler = TimedRotatingFileHandler(filename=filename, when='MIDNIGHT')
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def set_log_level(self, log_level):
        if log_level == 'error':
            self.logger.setLevel(logging.ERROR)
        elif log_level == 'debug':
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def check_root_dir(self):
        path = f'{self.base_dir}'
        if not os.path.exists(path):
            os.makedirs(path)

    def processing(self, msg):
        self.write('[processing] %s' % str(msg))

    def write(self, msg):
        if not isinstance(msg, str):
            try:
                msg = str(msg)
            except:
                msg = msg
        if self.logger.level == logging.ERROR:
            self.logger.error(msg)
        elif self.logger.level == logging.DEBUG:
            self.logger.debug(msg)
        else:
            self.logger.info(msg)


error_log = partial(MyLogging, log_name='error', file_name='error')
# server_log = MyLogging(log_name='server', file_name='server')
# time_log = MyLogging(log_name='time', file_name='time')
# statistics_log = MyLogging(log_name='statistics', file_name='statistics')
