
# FIXME: license

from PyQt5 import QtNetwork, QtCore

#_qt_network_manager = QtNetwork.QNetworkAccessManager()

API_BASE = "https://api.telegram.org/bot{token}/{method}"


class _Downloader(object):
    """An asynch downloader that fires a deferred with data when done."""
    def __init__(self, url):
        self.deferred = defer.Deferred()
        self.deferred._store_it_because_qt_needs_or_wont_work = self
        self.progress = 0
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))

        self.req = _qt_network_manager.get(request)
        self.req.error.connect(self.error)
        self.req.finished.connect(self.end)
        self.req.downloadProgress.connect(self._advance_progress)

    def error(self, error_code):
        """Request finished (*maybe*) on error."""
        if error_code != 5:
            # different to OperationCanceledError, so we didn't provoke it
            exc = RuntimeError("Network Error: " + self.req.errorString())
            self.deferred.errback(exc)

    def _advance_progress(self, dloaded, total):
        """Increment progress."""
        self.progress = dloaded

    def abort(self):
        """Abort the download."""
        self.req.abort()

    def end(self):
        """Send data through the deferred, if wasn't fired before."""
        img_data = self.req.read(self.req.bytesAvailable())
        content_type = self.req.header(
            QtNetwork.QNetworkRequest.ContentTypeHeader)
        data = (content_type, img_data)
        if not self.deferred.called:
            self.deferred.callback(data)


def get_messages(callback):
    print("===== get messssssssssages")

    # url = API_BASE.format(token=TOKEN, method="getUpdates")
    # print("=========url", url)
    # req = request.urlopen(url)
    # resp = req.read()
    # print("========= resp", repr(resp))
    def _get():
        # FIXME: get messages FOR REAL!!
        import time
        callback(["New messssssssage: " + time.ctime()])
        QtCore.QTimer.singleShot(1000, _get)  # FIXME: get polling time from config!

    _get()
