import requests as _r
from utils2.networking._context import PrePostFunction
from utils2.networking.downloadAdapter import adapter as _adapter_dl


class Session:
    def __init__(self, pre=None, post=None, headers=None):
        """A session is a wrapper around the requests.

        :param headers: The constant headers to send with all requests unless specified otherwise
        :param pre: A function to run before the request, will receive the URL as a parameter
        :param post: A function to run after the request, will receive the request object as a parameter
        """


        self._pre = pre
        self._post = post

        self._session = _r.session()
        self.headers = headers

    def _runPre(self, value):
        if self._pre is not None:
            self._pre(value)

    def _runPost(self, value):
        if self._post is not None:
            self._post(value)


    def get(self, url, headers=None, *args, **kwargs):

        if headers is None:
            headers = self.headers


        self._runPre(url)
        response = _r.get(url, headers=headers, *args, **kwargs)
        self._runPost(response)

        return response

    def post(self, url, data=None, json=None, headers=None, *args, **kwargs):
        if headers is None:
            headers = self.headers

        self._runPre(url)
        response = _r.post(url, data=data, json=json, headers=headers, *args, **kwargs)
        self._runPost(response)

        return response

    def changeHeaders(self, headers):
        self.headers = headers

    def injectCookie(self, name, value):
        self.session.cookies.set(name=name, value=value)

    @staticmethod
    def progressGet(filename: str, url: str):
        return _adapter_dl(url=url).download(filename=filename)

    @property
    def downloadAdapter(self):
        return _adapter_dl

    @property
    def session(self):
        """The requests session"""
        return self._session
