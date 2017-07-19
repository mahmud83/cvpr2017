import requests
import threading
from nutszebra_utility import Utility as utility


class Download(object):

    def __init__(self):
        pass

    @staticmethod
    def download_request(url, path, chunk_size=1024, timeout=5):
        try:
            res = requests.get(url, stream=True, timeout=timeout)
        except requests.exceptions.Timeout:
            return False
        except requests.exceptions.RequestException:
            return False
        except requests.exceptions.HTTPError:
            return False
        except requests.exceptions.ConnectionError:
            return False
        except:
            return False
        if res.status_code == 200:
            with open(path, 'wb') as file:
                for chunk in res.iter_content(chunk_size=chunk_size):
                    file.write(chunk)


class ThreadDownloadSlave(threading.Thread):

    def __init__(self, url, path, callback=None, arguments=None, chunk_size=1024, debug=False, timeout=5):
        super(ThreadDownloadSlave, self).__init__()
        self.url = url
        self.path = path
        self.callback = callback
        self.arguments = arguments
        self.chunk_size = chunk_size
        self.debug = debug
        self.timeout = timeout

    def run(self):
        try:
            if self.debug is True:
                print('start: ' + str(self.url))
            Download.download_request(self.url, self.path, chunk_size=self.chunk_size, timeout=self.timeout)
            if self.callback is not None:
                self.arguments['path'] = self.path
                self.callback(**self.arguments)
            if self.debug is True:
                print('end: ' + str(self.url))
        except:
            return False


class ThreadDownloadMaster(object):

    def __init__(self, howmany_thread=1000, urls=(), paths=(), arguments=(), callback=None, chunk_size=1024, debug=False, timeout=5):
        self.howmany_thread = howmany_thread
        self.urls = urls
        self.paths = paths
        if arguments == ():
            arguments = (None, ) * len(urls)
        self.arguments = arguments
        self.callback = callback
        self.chunk_size = chunk_size
        self.debug = debug
        self.timeout = timeout

    @staticmethod
    def _execute_thread(queue):
        [_.start() for _ in queue]
        [_.join() for _ in queue]

    def run(self):
        queue = []
        progressbar = utility.create_progressbar(len(self.urls), desc='files')
        for i in progressbar:
            queue.append(ThreadDownloadSlave(self.urls[i], self.paths[i], callback=self.callback, arguments=self.arguments[i], chunk_size=self.chunk_size, debug=self.debug, timeout=self.timeout))
            if len(queue) >= self.howmany_thread:
                self._execute_thread(queue)
                queue = []
        else:
            if len(queue) is not 0:
                self._execute_thread(queue)
