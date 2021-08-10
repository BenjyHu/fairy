'''
Author : hupeng
Time : 2021/8/6 15:09 
Description: 
''' 
import time
from functools import wraps


def cal_time(msg: str = None):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            t2 = time.time()
            if msg:
                print("\033[1;32m %s: %s secs. \033[0m" % (msg, t2 - t1))
            else:
                print("\033[1;32m %s running time: %s secs. \033[0m" % (func.__name__, t2 - t1))
            return result

        return inner

    return wrapper


def log_time(time_record, msg: str = None):
    '''
    记录模块时间
    只用于同步模块
    1、当作用于函数体时：
        @log_time('func执行时间')
        def func():
            pass

    2、当想记录函数体中部分逻辑时：
        from okay_ocr_svr.utils.log import time_record

        t = time.time()
        your code processing
        cost = time.time() - t
        time_record['执行时间'] = float('%.3f' % cost)

    并不需要额外写入到日志文件里
    '''
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            t2 = time.time()
            cost = float('%.3f' % (t2 - t1))
            time_record[msg or func.__name__] = cost
            return result

        return inner

    return wrapper
