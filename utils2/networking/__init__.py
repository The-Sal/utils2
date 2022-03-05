import requests as _r
from utils2.networking._context import PrePostFunction
from utils2.networking.downloadAdapter import adapter as _adapter_dl

class Session:
    def __init__(self, funcs=None, headers=None):
        """
            :param funcs A dictionary with 2 keys 'post' and 'pre' which contain 2 functions
            :param headers The constant headers to send with all requests unless specified otherwise
        """

        self.session = _r.session()
        self._preFunc = funcs['pre']
        self._postFunc = funcs['post']
        self.headers = headers



    def get(self, url, headers=None, *args, **kwargs):

        if headers is None:
            headers = self.headers

        p = PrePostFunction(self._preFunc, self.post)
        p.url = url

        with p:
            response = _r.get(url, headers=headers, *args, **kwargs)
            p.request = response

        return response

    def post(self, url, data=None, json=None, headers=None, *args, **kwargs):
        if headers is None:
            headers = self.headers

        p = PrePostFunction(self._preFunc, self.post)
        p.url = url

        with p:
            response = _r.post(url, data=data, json=json, headers=headers, *args, **kwargs)
            p.request = response

        return response

    def changeHeaders(self, headers):
        self.headers = headers

    def changePreFunc(self, func):
        self._preFunc = func

    def changePostFunc(self, func):
        self._postFunc = func

    def injectCookie(self, name, value):
        self.session.cookies.set(name=name, value=value)

    @staticmethod
    def progressGet(filename: str, url: str):
        return _adapter_dl(url=url).download(filename=filename)

    @property
    def downloadAdapter(self):
        return _adapter_dl