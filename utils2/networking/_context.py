class PrePostFunction:
    def __init__(self, pre, post):
        self.pre = pre
        self.post = post
        self.url = None
        self.request = None

    def __enter__(self):
        if self.pre is not None:
            self.pre(self.url)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.post is not None:
            self.post(self.request)