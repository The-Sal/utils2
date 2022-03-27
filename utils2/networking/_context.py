class PrePostFunction:
    def __init__(self, pre, post):
        self._pre = pre
        self._post = post
        self.url = None
        self.request = None

    def __enter__(self):
        if self._pre is not None:
            self._pre(self.url)

    def __exit__(self, exc_type, exc_value, traceback):
        if self._post is not None:
            self._post(self.request)
