import threading
import os

from analyze import process_exp1_file, process_exp2_file, process_exp3_file


class FileProcess(threading.Thread):
    """
    Simple thread wrapper for async process
    data files of each experiment
    """
    def __init__(self, func, filename, post_clean=True, **kwargs):
        threading.Thread.__init__(self)
        self.func = func
        self.filename = filename
        self.post_clean = post_clean
        self.kwargs = kwargs

    def run(self):
        """
        Call the given function to the given file
        with the arguments
        """
        self.func(self.filename, **self.kwargs)
        if self.post_clean:
            self.purge()

    def purge(self):
        """
        Delete the file hold by the thread
        if it exists
        """
        try:
            os.remove(self.filename)
        except OSError, e:
            raise e


def post_process(which, filename, **kwargs):
    """
    Main entry for the post process module
    """
    if which == 'exp1':
        return _async_exec(process_exp1_file, filename, **kwargs)
    elif which == 'exp2':
        return _async_exec(process_exp2_file, filename, **kwargs)
    elif which == 'exp3':
        return _async_exec(process_exp3_file, filename, **kwargs)
    else:
        raise ValueError('Illegal argument: %s' % which)


def _async_exec(func, filename, **kwargs):
    """
    Setting up a new thread and kick it off
    """
    t = FileProcess(func, filename, **kwargs)
    t.setName('thread-%s' % filename)
    t.start()
    return t


def wait_for(threads):
    """
    Waits until all threads in the given
    list finish
    """
    for t in threads:
        if t.isAlive():
            print 'Waiting for thread: %s' % t.getName()
            t.join()
