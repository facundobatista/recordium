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

import logging
import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from recordium import network, storage

logger = logging.getLogger(__name__)


# FIXME (bug): support receiving audios

ABOUT_TEXT = """
<center>
Send messages via Telegram that will be notified later in your desktop.<br/>
<br/>
Version {version}<br/>
<br/>
<small>Copyright 2016 Facundo Batista</small><br/>
<br/>
<a href="https://github.com/facundobatista/recordium">The project</a>
</center>
"""

N_MESSAGES_TEXT = "{quantity} new messages"


def debug_trace():
    '''Set a tracepoint in the Python debugger that works with Qt'''
    from PyQt5.QtCore import pyqtRemoveInputHook

    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()


class MessagesWidget(QtWidgets.QTableWidget):
    """The list of messages."""

    # FIXME: on windows closing, get the messages marked as done and call storage.delete_item
    # on them

    # keep this one as an attribute as it's used in several parts
    check_col = 2

    def __init__(self, storage, systray):
        self._messages = storage.get_elements()
        self._storage = storage
        self._systray = systray
        super().__init__(len(self._messages), 3)

        for row, msg in enumerate(self._messages):
            item = QtWidgets.QTableWidgetItem(str(msg.sent_at))
            self.setItem(row, 0, item)

            item = QtWidgets.QTableWidgetItem(msg.text)
            self.setItem(row, 1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.setItem(row, self.check_col, item)

        self.setHorizontalHeaderLabels(("When", "Text", "Done"))
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        # FIXME (bug): calculate height and width, and set window size to that with some limit (so
        # window doesn't get too big); if size trimmed, scrollbars should appear automatically)

        self.itemClicked.connect(self.item_clicked)
        self.show()

    def closeEvent(self, event):
        """Intercept closing and delete marked messages."""
        messages_to_remove = []
        for row in range(self.rowCount()):
            if self.item(row, self.check_col).checkState() == QtCore.Qt.Checked:
                # note, we can access the message like this because the table can not be reordered
                messages_to_remove.append(self._messages[row])
        if messages_to_remove:
            self._storage.delete_elements(messages_to_remove)
            self._systray.set_message_number()
        super().closeEvent(event)

    def item_clicked(self, widget):
        """An item in the table was clicked."""
        if widget.column() != 2:
            # not a checkbox
            return

        # FIXME: disable (put to grey) or enable the row, according to checkbox


class SysTray:
    def __init__(self, app, version):
        self.app = app
        self.version = version
        icon = QtGui.QIcon("media/icon-192.png")

        self.sti = sti = QtWidgets.QSystemTrayIcon(icon)
        self.menu = menu = QtWidgets.QMenu()
        self._messages_action = menu.addAction('')
        self.set_message_number()
        self._messages_action.triggered.connect(self._show_messages)
        menu.addSeparator()
        action = menu.addAction("Configure")
        action.triggered.connect(self._configure)
        action = menu.addAction("About")
        action.triggered.connect(self._about)
        action = menu.addAction("Quit")
        action.triggered.connect(lambda _: self.app.quit())
        sti.setContextMenu(menu)

        sti.show()

    def _configure(self, _):
        print("========= config")
        # FIXME: have a configuration settings, with:
        # - the token (default empty)
        # - the polling time (default 30s)

    def _about(self, _):
        """Show the About dialog."""
        version = self.version if self.version else "(?)"
        title = "Recordium v" + version
        text = ABOUT_TEXT.format(version=version)
        QtWidgets.QMessageBox.about(None, title, text)

    def _show_messages(self, _):
        """Show a window with the messages."""
        # store it in the instance otherwise it's destroyed
        self._temp_mw = MessagesWidget(self.app.storage, self)

    def set_message_number(self):
        """Set the message number in the systray icon."""
        # FIXME: change the icon color
        quantity = len(self.app.storage.get_elements())
        self._messages_action.setText(N_MESSAGES_TEXT.format(quantity=quantity))


class RecordiumApp(QtWidgets.QApplication):
    def __init__(self, version):
        super().__init__(sys.argv)
        self.setQuitOnLastWindowClosed(False)  # so app is not closed when closing other windows
        self.storage = storage.Storage()
        self.systray = SysTray(self, version)

        network.get_messages(self.new_messages, self.storage.get_last_element_id)

    def new_messages(self, messages):
        """Called FROM A THREAD when new messages are available."""
        self.storage.add_elements(messages)
        self.systray.set_message_number()


def go(version):
    app = RecordiumApp(version)
    sys.exit(app.exec_())
