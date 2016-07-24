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

FILEPATH = os.path.join(BaseDirectory.xdg_data_home, 'recordium.pkl')


class Storage:
    """Store the messages."""

    def __init__(self):
        if os.path.exists(FILEPATH):
            with open(FILEPATH, 'rb') as fh:
                self.data = pickle.load(fh)
            logger.debug("Loaded %d items", len(self.data))
        else:
            self.data = []
            logger.debug("File not found, starting empty")

    # FIXME: provide a method to remove messages older than N days

    def get_elements(self, including_viewed=False):
        pass
        # FIXME return all the elements, filtering by 'viewed'

    def set_viewed(self, element_id, viewed):
        pass
        # FIXME set viewed or not for the indicated element

    def add_elements(self, elements):
        pass
        # FIXME add a bunch of elements to the storage

    def _save(self):
        """Save the data to disk."""
        # we don't want to pickle this class, but the dict itself
        logger.debug("Saving %d items", len(self.data))
        with SafeSaver(FILEPATH) as fh:
            pickle.dump(self.data, fh)
