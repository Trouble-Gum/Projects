import redis

import config as cf
from extensions import log, INFO, ERROR

MAX_CACHE_SIZE = 10
CON_POOL_BUF_SIZE = 1000


# for usage as decorator
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


@singleton  # assurance that only one instance for the whole application will be used
class RedisSynchronizer:
    """ This class provides you contain MAX_CACHE_SIZE records with user-settings data
    and make batch-synchronization with redis only after achievement of this limit
    """

    def __init__(self):
        self._connection_pool = {
            'client_modes': {},
            'cache_amount': 0,
            'cached_records': []
        }

        self._rds = redis.Redis(  # redis connection
            host=cf.REDIS_HOST,
            port=cf.REDIS_PORT,
            password=cf.REDIS_PSW
        )

        log('RedisSynchronizer is initialized', INFO)

    @property
    def connection_pool(self):
        """returns dict with data of user-settings, current work modes"""
        return self._connection_pool

    def _clear_connection_pool(self):
        """releases memory after achievement CON_POOL_BUF_SIZE records in connection_pool"""
        if len(self.connection_pool['client_modes']) > CON_POOL_BUF_SIZE:
            self._connection_pool = {
                'client_modes': {},
                'cache_amount': 0,
                'cached_records': []
            }
            log('Connection pool is cleared', INFO)

    def synchronize_with_redis(self, force=False):
        """unload cached records to redis"""
        if self.connection_pool['cache_amount'] < MAX_CACHE_SIZE and not force:
            return
        else:
            for key, value in self.connection_pool['client_modes'].items():
                if key in self.connection_pool['cached_records']:
                    try:
                        self._rds.set(key, value)
                    except Exception as e:
                        log(e, ERROR)  # in case of error write it into log
                    else:
                        log('Synchronized successfully', INFO)
            self.connection_pool['cache_amount'] = 0
            self.connection_pool['cached_records'] = []
            self._clear_connection_pool()  # clear connection pool if there is a need (checks are inside method)

    def get_actual_user_mode(self, user):
        """returns actual user work mode"""
        try:
            result = self.connection_pool['client_modes'][user + '-mode']  # try to get it from memory
        except KeyError:
            mode = self._rds.get(user + '-mode')  # in case of error try to get it from redis
            try:
                result = str(mode, 'utf-8')
            except TypeError:
                result = None
            else:
                self.connection_pool['client_modes'][user + '-mode'] = result  # put it into cache immediately
        return result

    def put_user_mode_into_cache(self, user, mode):
        """writes new work mode of user into cache"""
        cur_mode = self.get_actual_user_mode(user)
        if cur_mode != mode:  # only in case when prev and next modes are not equal
            if user + '-mode' not in self.connection_pool['cached_records']:
                self.connection_pool['cache_amount'] += 1
                self.connection_pool['cached_records'].append(user + '-mode')

            self.connection_pool['client_modes'][user + '-mode'] = mode
            self.synchronize_with_redis()


rs = RedisSynchronizer()


def force_synchronize():
    try:
        rs.synchronize_with_redis(force=True)
    except Exception as e:
        log(e, ERROR)


if __name__ == '__main__':
    rds = redis.Redis(
        host=cf.REDIS_HOST,
        port=cf.REDIS_PORT,
        password=cf.REDIS_PSW
    )
    print('actual data in current redis instance: ', rds.keys())

    del_flag = input('to delete data from current redis db press y: ')
    if del_flag == 'y':
        rds.delete(*rds.keys())
        print(rds.keys())
