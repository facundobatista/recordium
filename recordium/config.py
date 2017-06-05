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
import os
import pickle

from recordium.utils import SafeSaver, config_basedir

logger = logging.getLogger(__name__)

FILEPATH = os.path.join(config_basedir, 'recordium.cfg')


class _Config(object):
    """The configuration."""

    # config options, with their default
    _config_options = {
        'BOT_AUTH_TOKEN': '',
        'POLLING_TIME': 30,
        'USER_ALLOWED': None,
        'COL_ORDER': []
    }
    _need_save = 0

    def __init__(self):
        if not os.path.exists(FILEPATH):
            # default to an empty dict
            logger.debug("File not found, starting empty")
            self.data = {}
            return

        with open(FILEPATH, 'rb') as fh:
            self.data = pickle.load(fh)
        logger.debug("Loaded: %s", self.data)

    def __getattr__(self, key):
        return self.data.get(key, self._config_options[key])

    def __setattr__(self, key, value):
        if key in self._config_options:
            if self.data.get(key) != value:
                self.data[key] = value
                self._need_save += 1
        else:
            if key.upper() != key:
                super(_Config, self).__setattr__(key, value)
            else:
                raise AttributeError

    def save(self):
        """Save the config to disk."""
        if self._need_save:
            logger.debug("Saving: %s", self.data)
            with SafeSaver(FILEPATH) as fh:
                pickle.dump(self.data, fh)
                self._need_save = 0


config = _Config()
