'''
Author : hupeng
Time : 2021/8/10 10:12 
Description: 
'''
import re
import typing as t


class Filter_Unkeywords(object):
    '''
    一次完成多个字符串替换
    利用正则表达式re的sub方法
    filter = Filter_Unkeywords(
        [r'\triangle',
        r'\square',
        r'\textcircled']
    )
    filter.multiple_replace(string)
    '''

    def __init__(self, r: t.List[str] = None):
        self.adict = {}
        r = r or []
        for i in r:
            self.adict[i] = ''

    def multiple_replace(self, text):
        rx = re.compile('|'.join(map(re.escape, self.adict)))

        def one_xlat(match):
            return self.adict[match.group(0)]

        # 每遇到一次匹配就会调用回调函数
        return rx.sub(one_xlat, text)
