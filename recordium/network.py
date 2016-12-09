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

from datetime import datetime
from urllib import parse

import defer

from PyQt5 import QtCore, QtNetwork

logger = logging.getLogger(__name__)

API_BASE = "https://api.telegram.org/bot{token}/{method}"


class NotificationItem:
    """The item shown in the notification."""

    def __init__(self, text, sent_at, message_id):
        self.text = text
        self.sent_at = sent_at
        self.message_id = message_id
        self.viewed = False

    @classmethod
    def from_update(cls, update):
        """Create from a telegram message."""
        update_id = int(update['update_id'])
        print("========= from up", update)
        try:
            msg = update['message']
        except KeyError:
            logger.warning("Unknown update type: %r", update)
            return

        text = msg['text']
        sent_at = datetime.fromtimestamp(msg['date'])
        return cls(text=text, sent_at=sent_at, message_id=update_id)


class NetworkError(Exception):
    """Problems in the network."""


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
        error_message = "Downloader error {}: {}".format(error_code, self.req.errorString())
        logger.warning(error_message)
        if not self.deferred.called:
            self.deferred.errback(NetworkError(error_message))

    def end(self):
        """Send data through the deferred, if wasn't fired before."""
        data = self.req.read(self.req.bytesAvailable())
        if data and not self.deferred.called:
            self.deferred.callback(data)


with open(os.path.join(os.path.expanduser("~"), ".recordium.token"), "rt", encoding="ascii") as fh:
    # FIXME: read this better from a config or something
    TOKEN = fh.read().strip()


def build_api_url(method, **kwargs):
    """Build the proper url to hit the API."""
    url = API_BASE.format(token=TOKEN, method=method)  # FIXME: get token from config
    if kwargs:
        url += '?' + parse.urlencode(kwargs)
    return url


def get_messages(new_items_callback, last_id_callback):
    """Get messages."""

    def _process(encoded_data):
        """Process received info."""
        data = json.loads(encoded_data.decode('utf8'))
        if data.get('ok'):
            items = []
            for item in data['result']:
                logger.debug("Processing result: %s", item)
                ni = NotificationItem.from_update(item)
                if ni is not None:
                    items.append(ni)
            if items:
                new_items_callback(items)
        else:
            logger.warning("Telegram result is not ok: %s", data)

    def _get():
        """Get the info from Telegram."""
        last_id = last_id_callback()
        kwargs = {}
        if last_id is not None:
            kwargs['offset'] = last_id + 1
        url = build_api_url('getUpdates', **kwargs)
        logger.debug("Getting updates: %s", kwargs)

        downloader = _Downloader(url)
        downloader.deferred.add_callback(_process)
        downloader.deferred.add_callbacks(
            lambda _: QtCore.QTimer.singleShot(1000, _get))  # FIXME: get polling time from config!

    QtCore.QTimer.singleShot(0, _get)
