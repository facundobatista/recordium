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


class _Config(dict):
    """The configuration."""

    def __init__(self):
        super().__init__()

        if not os.path.exists(FILEPATH):
            # default to an empty dict
            logger.debug("File not found, starting empty")
            return

        with open(FILEPATH, 'rb') as fh:
            saved_dict = pickle.load(fh)
        self.update(saved_dict)
        logger.debug("Loaded: %s", self)

    def save(self):
        """Save the config to disk."""
        # we don't want to pickle this class, but the dict itself
        raw_dict = self.copy()
        logger.debug("Saving: %s", self)
        with SafeSaver(FILEPATH) as fh:
            pickle.dump(raw_dict, fh)


config = _Config()
