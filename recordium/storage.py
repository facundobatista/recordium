# FIXME: license

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
        fixme
        # FIXME

    def set_viewed(self, element_id):
        fixme
        # FIXME

    def add_elements(self, elements):
        fixme
        # FIXME

    def _save(self):
        """Save the data to disk."""
        # we don't want to pickle this class, but the dict itself
        logger.debug("Saving %d items", len(self.data))
        with SafeSaver(FILEPATH) as fh:
            pickle.dump(self.data, fh)
