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

from PyQt5 import QtWidgets, QtGui

from recordium import network, storage

logger = logging.getLogger(__name__)


# FIXME: implement a window listing all messages
#  - provide a checkbox "Include reviewed messages"
#  - build the window with app.get_elements(including_viewed=?) <-- depends of the checkbox
#  - the state of the checkbox should go to the config
#  - we should have a button on each row, a checkbox, or something, to mark them as reviewed
#  - only when windows is closed those marked/unmarked are updated in the storage

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


class SysTray:
    def __init__(self, app, version):
        self.app = app
        self.version = version
        icon = QtGui.QIcon("media/icon-192.png")

        self.sti = sti = QtWidgets.QSystemTrayIcon(icon)
        self.menu = menu = QtWidgets.QMenu()
        # FIXME: always start with 0? NO!!
        self._messages_action = menu.addAction(N_MESSAGES_TEXT.format(quantity=0))
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
        print("========= messa")
        # FIXME: open the window of messages

    def set_message_number(self, quantity):
        print("======== set message quantity!", quantity)
        # FIXME: change the icon color
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
        self.systray.set_message_number(len(self.storage.get_elements()))


def go(version):
    app = RecordiumApp(version)
    sys.exit(app.exec_())
