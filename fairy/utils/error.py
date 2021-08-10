'''
Author : hupeng
Time : 2021/8/9 14:44 
Description: 
''' 
class ParametersError(ValueError):
    '''参数错误'''
    pass


class RegularError(BaseException):
    '''正则匹配错误'''
    pass


class SimilarityError(BaseException):
    '''相似度错误'''
    pass


class ServerError(BaseException):
    pass


class TimeoutError(Exception):
    pass


class ApiError(Exception):
    pass
