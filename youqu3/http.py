from youqu3 import logger
from youqu3.exceptions import YouQuPluginDependencyError

try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

if HAS_REQUESTS is False:
    raise YouQuPluginDependencyError("requests")


class Session:

    def __init__(self) -> None:
        self.session = requests.Session()

    def get(self, url, params=None, **kwargs):
        logger.debug(f'GET {url}')
        if params:
            logger.debug(f'params {params}')
        if kwargs:
            logger.debug(kwargs)
        return self.session.get(url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        logger.debug(f'POST {url}')
        if data:
            logger.debug(f'data {data}')
        if json:
            logger.debug(f'json {json}')
        if kwargs:
            logger.debug(kwargs)
        return self.session.post(url, data=data, json=json, **kwargs)

if __name__ == '__main__':
    Session().post(url="").json()