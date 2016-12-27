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

ELEMENTS = 'elements'
LAST_ELEMENT_ID = 'last_elements_id'


class Storage:
    """Store the messages."""

    def __init__(self):
        if os.path.exists(FILEPATH):
            logger.debug("Loading from %r", FILEPATH)
            with open(FILEPATH, 'rb') as fh:
                self.data = pickle.load(fh)
        else:
            self.data = {
                ELEMENTS: {},
                LAST_ELEMENT_ID: None,
            }
            logger.debug("File not found, starting empty")

    def get_last_element_id(self):
        """Return the last stored element, None if nothing stored."""
        return self.data[LAST_ELEMENT_ID]

    def get_elements(self):
        """Return the elements."""
        elements = [element for _, element in sorted(self.data[ELEMENTS].items())]
        return elements

    def delete_elements(self, elements):
        """Remove elements from the storage."""
        logger.debug("Deleting elements: %s", elements)
        for element in elements:
            del self.data[ELEMENTS][element.message_id]
        self._save()

    def add_elements(self, elements):
        """Add the new elements (or replace them) to the storage."""
        logger.debug("Adding elements: %s", elements)
        new_elements_dict = {elem.message_id: elem for elem in elements}
        self.data[ELEMENTS].update(new_elements_dict)
        self.data[LAST_ELEMENT_ID] = max(new_elements_dict)
        self._save()

    def _save(self):
        """Save the data to disk."""
        # we don't want to pickle this class, but the dict itself
        logger.debug("Saving in %r", FILEPATH)
        with SafeSaver(FILEPATH) as fh:
            pickle.dump(self.data, fh)
