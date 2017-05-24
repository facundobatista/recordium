# Copyright 2016-2017 Facundo Batista
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
import platform
import os
import subprocess
import sys

from functools import lru_cache

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import __file__ as pyqt_path

from recordium import network, storage
from recordium.config import config

logger = logging.getLogger(__name__)


def fix_environment():
    """Add enviroment variable on Windows systems."""
    if platform.system() == "Windows":
        pyqt = os.path.dirname(pyqt_path)
        qt_platform_plugins_path = os.path.join(pyqt, "plugins")
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_platform_plugins_path


# the text to show in the About window
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

# the text to build the systray menu
N_MESSAGES_TEXT = "{quantity} new messages"

# icons to show if there are messages or not
ICONPATH_NO_MESSAGE = 'media/icon-recordium-192.png'
ICONPATH_HAVE_MESSAGES = 'media/icon-recordium-active-192.png'
ICONPATH_PROBLEM = 'media/icon-recordium-problem-192.png'

# icons for the messages GUI
ICONPATH_IMAGE = 'media/icon-picture.png'
ICONPATH_AUDIO = 'media/icon-sound.png'
ICONPATH_MEDIA_UNKNOWN = 'media/icon-mediaunknown.png'


def debug_trace():
    """Set a tracepoint in the Python debugger that works with Qt."""
    from PyQt5.QtCore import pyqtRemoveInputHook

    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()


class ConfigWidget(QtWidgets.QDialog):
    """The config window."""

    _msg_user_not_set = "Not configured yet, will be set with the first message received"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration")

        main_layout = QtWidgets.QVBoxLayout()
        if not config.BOT_AUTH_TOKEN:
            main_layout.addWidget(QtWidgets.QLabel(
                "Please configure Recordium to be able to start fetching messages\n"
                "See instructions on README.rst"), 0)
            hline = QtWidgets.QFrame()
            hline.setFrameShape(QtWidgets.QFrame.HLine)
            hline.setFrameShadow(QtWidgets.QFrame.Sunken)
            main_layout.addWidget(hline)

        self.grid = grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel("Telegram bot auth token:"), 0, 0)  # row 0, col 0
        prev = config.BOT_AUTH_TOKEN
        self.entry_auth_token = QtWidgets.QLineEdit(prev)
        grid.addWidget(self.entry_auth_token, 0, 1, 1, 2)  # row 0, cols 1 and 2

        grid.addWidget(QtWidgets.QLabel("Polling time (in seconds, min=1):"), 1, 0)  # row 1, col 0
        prev = config.POLLING_TIME
        self.entry_polling_time = QtWidgets.QSpinBox()
        self.entry_polling_time.setValue(prev)
        self.entry_polling_time.setMinimum(1)
        grid.addWidget(self.entry_polling_time, 1, 1, 1, 2)  # row 1, cols 1 and 2

        grid.addWidget(QtWidgets.QLabel("Allowed user id to send messages:"), 2, 0)  # row 2, col 0
        self._user_reset_button = QtWidgets.QPushButton("Reset")
        self._user_reset_button.clicked.connect(self._user_reset)
        grid.addWidget(self._user_reset_button, 2, 2)  # row 2, col 2
        user_config = config.USER_ALLOWED
        if user_config is None:
            user_config = self._msg_user_not_set
            self._user_reset_button.setEnabled(False)
        else:
            user_config = str(user_config)
        self._user_reset_label = QtWidgets.QLabel(user_config)
        grid.addWidget(self._user_reset_label, 2, 1)  # row 2, col 1

        main_layout.addLayout(grid, 0)
        main_layout.addStretch(1)

        self.setLayout(main_layout)
        self.show()

    def _user_reset(self, _):
        """Reset the allowed user."""
        # config will be saved on dialog closing
        config.USER_ALLOWED = None
        self._user_reset_button.setEnabled(False)

        # hide previous label and set the new one
        self._user_reset_label.hide()
        self._user_reset_label = QtWidgets.QLabel(self._msg_user_not_set)
        self.grid.addWidget(self._user_reset_label, 2, 1)  # row 2, col 1

    def closeEvent(self, event):
        """Intercept closing and save config."""
        config.BOT_AUTH_TOKEN = self.entry_auth_token.text().strip()
        config.POLLING_TIME = self.entry_polling_time.value()
        config.save()
        super().closeEvent(event)


class MessagesWidget(QtWidgets.QTableWidget):
    """The list of messages."""

    # useful columns (to not use just numbers in the code), and titles
    text_col = 1
    media_col = 2
    check_col = 3
    titles = ("When", "Text", "Media", "Done")

    # what to present when the user hovers the cells
    tooltips_present = [
        "When the message was sent",
        "The text of the message (double click to copy to the clipboard)",
        "The media (image, audio, etc) included in the message",
        "Select to remove the message from the system",
    ]
    tooltips_missing = [
        None,
        "No text included in the message",
        "No media included in the message",
        None,
    ]

    def __init__(self, storage, systray):
        self._messages = storage.get_elements()
        self._storage = storage
        self._systray = systray
        super().__init__(len(self._messages), len(self.titles))

        item_builders = [
            self._build_item_datetime,
            self._build_item_text,
            self._build_item_media,
            self._build_item_checkbox,
        ]

        for row, msg in enumerate(self._messages):
            logger.debug("Set message for row %d: %s", row, msg)
            for col in range(len(self.titles)):
                # get the builder according to the column and build the item
                builder = item_builders[col]
                item = builder(msg)

                # if no specific item, build and empty one, and add a tooltip in any case
                if item is None:
                    item = QtWidgets.QTableWidgetItem()
                    item.setToolTip(self.tooltips_missing[col])
                else:
                    item.setToolTip(self.tooltips_present[col])

                # set it to not editable and put it in the table
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.setItem(row, col, item)

        self.setHorizontalHeaderLabels(self.titles)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSizeAdjustPolicy(2)

        # enable user to move columns
        header = self.horizontalHeader()
        header.setSectionsMovable(True)
        
        # load configuration & put columns in saved order
        for fr, to in enumerate(config.COL_ORDER):
            header.moveSection(self.visualColumn(fr), to)

        self.itemClicked.connect(self._item_clicked)
        self.itemDoubleClicked.connect(self._item_doubleclicked)
        self.show()

    def _build_item_datetime(self, msg):
        """Build the item for the datetime column."""
        return QtWidgets.QTableWidgetItem(str(msg.sent_at))

    def _build_item_text(self, msg):
        """Build the item for the text column."""
        if msg.text is not None:
            return QtWidgets.QTableWidgetItem(msg.text)

    def _build_item_media(self, msg):
        """Build the item for the media column."""
        if msg.extfile_path is not None:
            # build the icon according to the media type, if known
            if msg.media_type == msg.MEDIA_TYPE_IMAGE:
                icon = QtGui.QIcon(ICONPATH_IMAGE)
            elif msg.media_type == msg.MEDIA_TYPE_AUDIO:
                icon = QtGui.QIcon(ICONPATH_AUDIO)
            else:
                icon = QtGui.QIcon(ICONPATH_MEDIA_UNKNOWN)

            item = QtWidgets.QTableWidgetItem()
            item.setIcon(icon)
            return item

    def _build_item_checkbox(self, msg):
        """Build the item for the checkbox column."""
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)
        return item

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

        # saves column order configuration
        col_order = []
        for col in range(self.columnCount()):
            col_order.append(self.visualColumn(col))
        config.COL_ORDER = col_order
        config.save()
        super().closeEvent(event)

    def _item_clicked(self, widget):
        """An item in the table was clicked."""
        column = widget.column()
        row = widget.row()

        if column == self.check_col:
            # click in the checkbox column disable or enable the whole row
            disable = widget.checkState() == QtCore.Qt.Checked
            for column in range(len(self.titles) - 1):  # -1 to not strike out checkbox
                item = self.item(row, column)
                if disable:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                else:
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsEnabled)
                font = item.font()
                font.setStrikeOut(disable)
                item.setFont(font)

    def _item_doubleclicked(self, widget):
        """An item in the table was clicked."""
        column = widget.column()
        row = widget.row()

        if column == self.media_col:
            # click in the media column, execute externally
            msg = self._messages[row]
            if msg.extfile_path is not None:
                logger.debug("Opening external file %r", msg.extfile_path)
                subprocess.call(['/usr/bin/xdg-open', msg.extfile_path])

        elif column == self.text_col:
            # click in the text column, copy to clipboard
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(widget.text())


class SysTray:
    def __init__(self, app, version):
        self.app = app
        self.version = version

        # build the icon and message line, which will be properly set below when calling the
        # set_message_number() method
        self.sti = sti = QtWidgets.QSystemTrayIcon()
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
        """Show the configuration dialog."""
        self._temp_cw = ConfigWidget()
        self._temp_cw.exec_()

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

    @lru_cache(None)
    def _get_icon(self, have_messages):
        """Return and cache an icon."""
        if not config.BOT_AUTH_TOKEN:
            path = ICONPATH_PROBLEM
        elif have_messages:
            path = ICONPATH_HAVE_MESSAGES
        else:
            path = ICONPATH_NO_MESSAGE
        return QtGui.QIcon(path)

    def set_message_number(self):
        """Set the message number in the systray icon."""
        quantity = len(self.app.storage.get_elements())
        self._messages_action.setText(N_MESSAGES_TEXT.format(quantity=quantity))
        self.sti.setIcon(self._get_icon(bool(quantity)))
        self._messages_action.setEnabled(bool(quantity))


class RecordiumApp(QtWidgets.QApplication):
    def __init__(self, version):
        super().__init__(sys.argv)
        if not config.BOT_AUTH_TOKEN:
            self._temp_cw = ConfigWidget()
            self._temp_cw.exec_()
        self.setQuitOnLastWindowClosed(False)  # so app is not closed when closing other windows
        self.storage = storage.Storage()
        self.systray = SysTray(self, version)
        self.messages_getter = network.MessagesGetter(
            self._new_messages, self.storage.get_last_element_id)
        self.messages_getter.go()

    def _new_messages(self, messages):
        """Called when new messages are available."""
        self.storage.add_elements(messages)
        self.systray.set_message_number()


def go(version):
    fix_environment()
    app = RecordiumApp(version)
    sys.exit(app.exec_())
