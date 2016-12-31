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

from datetime import datetime
from urllib import parse

import defer

from PyQt5 import QtCore, QtNetwork

from recordium.config import config

logger = logging.getLogger(__name__)

API_BASE = "https://api.telegram.org/bot{token}/{method}"


class NotificationItem:
    """The item shown in the notification."""

    def __init__(self, text, sent_at, message_id):
        self.text = text
        self.sent_at = sent_at
        self.message_id = message_id

    @classmethod
    def from_update(cls, update):
        """Create from a telegram message."""
        update_id = int(update['update_id'])
        try:
            msg = update['message']
        except KeyError:
            logger.warning("Unknown update type: %r", update)
            return

        text = msg['text']
        sent_at = datetime.fromtimestamp(msg['date'])
        return cls(text=text, sent_at=sent_at, message_id=update_id)

    def __str__(self):
        return "<Message [{}] {} {!r}>".format(self.message_id, self.sent_at, self. text)


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


def build_api_url(method, **kwargs):
    """Build the proper url to hit the API."""
    token = config.get(config.BOT_AUTH_TOKEN)
    url = API_BASE.format(token=token, method=method)
    if kwargs:
        url += '?' + parse.urlencode(kwargs)
    return url


class MessagesGetter:
    """Get messages."""

    def __init__(self, new_items_callback, last_id_callback):
        self.new_items_callback = new_items_callback
        self.last_id_callback = last_id_callback

    def _process(self, encoded_data):
        """Process received info."""
        logger.debug("Process encoded data len=%d", len(encoded_data))
        data = json.loads(encoded_data.decode('utf8'))
        if data.get('ok'):
            results = data['result']
            logger.debug("Telegram results ok! len=%d", len(results))
            items = []
            for item in results:
                logger.debug("Processing result: %s", item)
                ni = NotificationItem.from_update(item)
                if ni is not None:
                    items.append(ni)
            if items:
                self.new_items_callback(items)
        else:
            logger.warning("Telegram result is not ok: %s", data)

    def go(self):
        """Get the info from Telegram."""
        last_id = self.last_id_callback()
        kwargs = {}
        if last_id is not None:
            kwargs['offset'] = last_id + 1
        url = build_api_url('getUpdates', **kwargs)
        logger.debug("Getting updates, kwargs=%s", kwargs)

        def _re_get(error):
            """Capture all results; always re-issue self.go, if error raise it."""
            polling_time = 1000 * config.get(config.POLLING_TIME)
            logger.debug("Re get, error=%s polling_time=%d", error, polling_time)
            QtCore.QTimer.singleShot(polling_time, self.go)
            if error is not None:
                error.raise_exception()

        self._downloader = _Downloader(url)
        self._downloader.deferred.add_callback(self._process)
        self._downloader.deferred.add_callbacks(_re_get, _re_get)
