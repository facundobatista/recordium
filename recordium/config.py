# FIXME: license

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
