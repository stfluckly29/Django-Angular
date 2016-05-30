import redis
from datetime import datetime


class RequestLogger(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.path.index('/api/') == 0 and len(request.path) > 5:
                flag = False
                r = redis.StrictRedis()
                today = datetime.now().strftime('%Y-%m-%d')
                _key = '%s::%s %s' % (today, request.method, request.path)
                if not r.get(_key):
                    flag = True
                r.incrby(_key)
                if flag:
                    r.expire(_key, 3600*24*30)
        except:
            pass

        return None