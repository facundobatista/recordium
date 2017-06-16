# Copyright 2017 Facundo Batista
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

import os
from unittest import TestCase, mock

from recordium import config

class TestConfig(TestCase):
    """Tests for config module."""
    TEMP_FILENAME = "/tmp/recordium.cfg"

    def setUp(self):
        """Set up. Patch FILEPATH. Creates a fake config."""
        self.config_patch = mock.patch("recordium.config.FILEPATH")
        config.FILEPATH = self.config_patch.start()
        config.FILEPATH = self.TEMP_FILENAME
        self.config_test = config._Config()

    def tearDown(self):
        """Remove temporary config file."""
        if os.path.exists(self.TEMP_FILENAME):
            os.remove(self.TEMP_FILENAME)
        self.config_patch.stop()

    def test_set(self):
        """Basic test: setting and getting a key."""
        newvalue = 15784651
        assert self.config_test.POLLING_TIME != newvalue
        self.config_test.POLLING_TIME = newvalue
        self.assertEqual(self.config_test.POLLING_TIME, newvalue)

    def test_attribute_error(self):
        """Try to access a non-existent attribute to raise an error."""
        try:
            self.config_test.SARASA = 1
        except AttributeError:
            pass
        else:
            self.assertTrue(False, "shouldn't access non-existent attribute")

    def test_create_hidden_attr(self):
        """Try to create a non-existent hidden attribute to check if pass."""
        try:
            self.config_test._new = 1
        except AttributeError:
            self.assertTrue(False, "if the new attribute is hidden, it should be created")

    def test_add_new_config(self):
        """Add a new config, using some that is None by default, & check if it will be saved."""
        assert self.config_test.USER_ALLOWED is None
        assert self.config_test._needs_save == 0

        self.config_test.USER_ALLOWED = None    # force value, equal to default

        self.assertNotEqual(self.config_test._needs_save, 0, "It has to be flagged to be saved")

    def test_overwritting_default_None_value(self):
        """Overwritten a default value with None, testing if it is saved."""
        old_default = self.config_test.POLLING_TIME
        assert old_default is not None

        self.config_test.POLLING_TIME = None
        self.config_test.save()

        cfg = config._Config()
        self.assertEqual(cfg.POLLING_TIME, None)

    def test_save(self):
        """Save a new configuration and reopen the file to test saving."""
        newvalue = "libertad"

        assert self.config_test.USER_ALLOWED != newvalue
        self.config_test.USER_ALLOWED = newvalue
        self.config_test.save()

        cfg = config._Config()
        self.assertEqual(cfg.USER_ALLOWED, newvalue)



