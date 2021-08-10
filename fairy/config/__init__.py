'''
Author : hupeng
Time : 2021/8/9 11:09 
Description: 
'''
from . import configparse
from kazoo.client import KazooClient


localconfig = configparse.ConfigParser()


class ZKHelper(object):
    def __init__(self, zk_host: str, zk_path: str):
        self._zk = KazooClient(zk_host)
        self.zk_path = zk_path

    def __enter__(self):
        self._zk.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._zk.stop()

    def get(self, path, space=False):
        path = '{}{}'.format(self.zk_path, path)
        value = self._zk.get(path)[0].decode()
        if space:
            return value
        return value.strip()

    def set_properties(self):
        children = self._zk.get_children(self.zk_path)
        for key in children:
            name = key.replace('.', '_')
            setattr(self, name, self.get(key))
