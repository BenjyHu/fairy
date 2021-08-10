'''
Author : hupeng
Time : 2021/8/10 10:19 
Description: 
'''
import time
import multiprocessing
from collections import defaultdict, OrderedDict
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor


class MultiPool(object):
    def __init__(self, max_workers=None, initializer=None, initargs=(),
                 maxtasksperchild=None):
        if max_workers is None:
            max_workers = cpu_count()

        multiprocessing.freeze_support()
        self.pool = multiprocessing.Pool(processes=max_workers, initializer=initializer, initargs=initargs,
                                         maxtasksperchild=maxtasksperchild)

    def submit(self, func, args=(), callback=None,
               error_callback=None, **kwargs):
        return self.pool.apply_async(func, args=args, kwds=kwargs, callback=callback,
                                     error_callback=error_callback)

    def close(self):
        return self.pool.close()

    def join(self):
        return self.pool.join()


class ThreadPool(object):
    def __init__(self):
        self.pool = ThreadPoolExecutor()

    def __call__(self, *args, **kwargs):
        return self.pool


thread_pool = ThreadPool()


class GeneralAsync(object):
    __POOL = {'thread': thread_pool, 'process': MultiPool}

    def __init__(self, num_processor=None, mode='thread'):
        self._funcs = []
        self.num_processor = num_processor
        self.mode = mode
        assert mode in self.__POOL, \
            f'mode param must be `thread` or `process`, but given {mode}'

    def __getattr__(self, item):
        pass

    def _pool(self, **kwargs):
        return self.__POOL[self.mode](**kwargs)

    def add_func(self, func, f_name=None, **params):
        '''
        追加并行执行的任务
        :param func: func
        :param params: param1, param2
        :return:
        '''
        assert callable(func), 'func object must be callable'
        params['func'] = func
        params['f_name'] = f_name or func.__name__
        self._funcs.append(params)

    def run(self):
        task = OrderedDict()
        response = defaultdict(list)
        pool = self._pool(max_workers=len(self._funcs))

        for func_info in self._funcs:
            func = func_info.pop('func')
            f_name = func_info.pop('f_name')
            task[f_name] = pool.submit(func, **func_info)

        if self.mode == 'process':
            pool.close()
            pool.join()

        for name, t in task.items():
            result = t.result() if hasattr(t, 'result') else t.get()
            setattr(self, name, result)
            response[name].append(result)
        return response
