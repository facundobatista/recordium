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
#  - get the messages from self.app.storage
#  - provide a checkbox "Include reviewed messages"
#  - build the window with app.get_elements(including_viewed=?) <-- depends of the checkbox
#  - the state of the checkbox should go to the config
#  - we should have a button on each row, a checkbox, or something, to mark them as reviewed
#  - only when windows is closed those marked/unmarked are updated in the storage


class SysTray:
    def __init__(self, app):
        self.app = app
        icon = QtGui.QIcon("media/icon-192.png")

        self.sti = sti = QtWidgets.QSystemTrayIcon(icon)
        self.menu = menu = QtWidgets.QMenu()
        action = menu.addAction("N messages")
        action.triggered.connect(self._show_messages)
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
        print("========= about")
        # FIXME: show a very similar about than Encuentro

    def _show_messages(self, _):
        print("========= messa")
        # FIXME: open the window of messages

    def set_message_number(self, quantity):
        print("======== set message quantity!", quantity)
        # FIXME: change the icon color
        # FIXME: change the menu entry to shown proper N messages


class RecordiumApp(QtWidgets.QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        network.get_messages(self.new_messages)
        self.systray = SysTray(self)
        self.storage = storage.Storage()

    def new_messages(self, messages):
        """Called FROM A THREAD when new messages are available."""
        print("=========== got new messages!!!", messages)
        self.storage.add_elements(messages)
        self.systray.set_message_number(len(self.storage.get_elements()))


def go(version):
    print("========0go 0")
    app = RecordiumApp()
    print("========0go 1")
    sys.exit(app.exec_())
    print("========0go 2")
