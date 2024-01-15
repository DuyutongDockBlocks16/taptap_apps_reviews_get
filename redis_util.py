# @Time : 2021/11/30 14:39
# @Author : zhanghan
# @File : redis_util.py
# @Desc: 操作redis的

import redis


class RedisUtil:

    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    ''' 产生用于redis的key
        :param  busi_id   业务id
        :param  key 当前数值的key
    '''

    def get_redis_key(self, busiid, key):
        return str(busiid) + '__' + str(key)

    def set(self, busiid, key, v):
        self.r.set(self.get_redis_key(busiid, key), v)

    def get(self, busiid, key):
        k = self.get_redis_key(busiid, key)
        return self.r.get(k)


REDIS_UTIL = RedisUtil()
