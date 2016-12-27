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
import os
import pickle

from xdg import BaseDirectory

from recordium.utils import SafeSaver

logger = logging.getLogger(__name__)

FILEPATH = os.path.join(BaseDirectory.xdg_config_home, 'recordium.cfg')


def _options_setter(cls):
    """Set the options as an attribute."""
    for name in cls._config_options:
        setattr(cls, name, name)
    return cls


@_options_setter
class _Config(object):
    """The configuration."""

    # config options, with their default
    _config_options = {
        'BOT_AUTH_TOKEN': '',
        'POLLING_TIME': 30,
    }

    def __init__(self):
        if not os.path.exists(FILEPATH):
            # default to an empty dict
            logger.debug("File not found, starting empty")
            self.data = {}
            return

        with open(FILEPATH, 'rb') as fh:
            self.data = pickle.load(fh)
        logger.debug("Loaded: %s", self.data)

    def get(self, key):
        return self.data.get(key, self._config_options[key])

    def set(self, key, value):
        self.data[key] = value

    def save(self):
        """Save the config to disk."""
        logger.debug("Saving: %s", self.data)
        with SafeSaver(FILEPATH) as fh:
            pickle.dump(self.data, fh)


config = _Config()
