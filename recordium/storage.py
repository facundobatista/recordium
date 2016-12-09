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


class Storage:
    """Store the messages."""

    def __init__(self):
        if os.path.exists(FILEPATH):
            with open(FILEPATH, 'rb') as fh:
                self.data = pickle.load(fh)
            logger.debug("Loaded %d items", len(self.data))
        else:
            self.data = {
                ELEMENTS: {},
            }
            logger.debug("File not found, starting empty")

    # FIXME: provide a method to remove messages older than N days

    def get_last_element_id(self):
        """Return the last stored element, None if nothing stored."""
        if not self.data[ELEMENTS]:
            return
        return max(self.data[ELEMENTS])

    def get_elements(self, including_viewed=False):
        """Return the elements, filtering by viewed."""
        elements = []
        for _, element in sorted(self.data[ELEMENTS].items()):
            if element.viewed and not including_viewed:
                continue
            elements.append(element)
        return elements

    def set_element(self, element):
        """Add the new element (or replace current one) to the storage."""
        logger.debug("Setting element: %s", element)
        self.data[ELEMENTS][element.message_id] = element
        self._save()

    def add_elements(self, elements):
        """Add the new elements (or replace them) to the storage."""
        logger.debug("Adding elements: %s", elements)
        self.data[ELEMENTS].update({elem.message_id: elem for elem in elements})
        self._save()

    def _save(self):
        """Save the data to disk."""
        # we don't want to pickle this class, but the dict itself
        logger.debug("Saving in %s", FILEPATH)
        with SafeSaver(FILEPATH) as fh:
            pickle.dump(self.data, fh)
