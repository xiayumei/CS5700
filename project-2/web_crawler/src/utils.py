import time as t


class Timer:
    """
    Context manager class for easily measuring timing
    """
    def __enter__(self):
        self.begin = t.time()
        return self

    def __exit__(self, *args):
        self.duration = t.time() - self.begin
