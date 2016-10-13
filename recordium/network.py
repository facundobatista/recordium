# Copyright 2016 Facundo Batista
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  https://github.com/facundobatista/recordium

import json
import logging
import os

import defer

from PyQt5 import QtCore, QtNetwork

logger = logging.getLogger(__name__)

API_BASE = "https://api.telegram.org/bot{token}/{method}"


class _Downloader(object):
    """An asynch downloader that fires a deferred with data when done."""

    def __init__(self, url):
        self._qt_network_manager = QtNetwork.QNetworkAccessManager()

        self.deferred = defer.Deferred()
        self.deferred._store_it_because_qt_needs_or_wont_work = self
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))

        self.req = self._qt_network_manager.get(request)
        self.req.error.connect(self.error)
        self.req.finished.connect(self.end)

    def error(self, error_code):
        """Request finished (*maybe*) on error."""
        logger.debug("Network error: %s", error_code)

    def end(self):
        """Send data through the deferred, if wasn't fired before."""
        data = self.req.read(self.req.bytesAvailable())
        if data and not self.deferred.called:
            self.deferred.callback(data)


with open(os.path.join(os.path.expanduser("~"), ".recordium.token"), "rt", encoding="ascii") as fh:
    # FIXME: read this better from a config or something
    TOKEN = fh.read().strip()


def get_messages(callback):
    url = API_BASE.format(token=TOKEN, method="getUpdates")  # FIXME: get token from config

    def _process(encoded_data):
        data = json.loads(encoded_data.decode('utf8'))
        print("========= FRUTA", data)
        if data.get('ok') is None:
            logger.warning("Telegram result is not ok: %s", data)
            return
        for item in data:
            print("==== item", item)
        # [{"update_id":693209741,\n"message":{"message_id":5,"from":{"id":425513,"first_name":"Facundo","last_name":"Batista","username":"facundobatista"},"chat":{"id":425513,"first_name":"Facundo","last_name":"Batista","username":"facundobatista","type":"private"},"date":1475257028,"text":"asd"}}]}'

    def _get():
        print("=========== _get")
        downloader = _Downloader(url)
        downloader.deferred.add_callback(_process)
        print("=========== def", downloader.deferred)
        QtCore.QTimer.singleShot(1000, _get)  # FIXME: get polling time from config!

    QtCore.QTimer.singleShot(0, _get)
