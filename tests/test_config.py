# Copyright 2016-2017 Facundo Batista, María Andrea Vignau
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
from unittest import TestCase

from recordium import config

class TestConfig(TestCase):
    """Tests for config module."""

    def setUp(self):
        """Set up. Creates a fake config"""
        self.config_test = _Config()

    def test_set(self):
        """Basic test: setting and getting a key"""
        newvalue = 15
        self.assertNotEqual(self.config_test.POLLING_TIME, newvalue)
        self.config_test.POLLING_TIME = newvalue
        self.assertEqual(self.config_test.POLLING_TIME, newvalue)

    def test_attribute_error(self):
        """Try to access an inexistent attribute to raise an error"""
        self.assertRaises(AttributeError, exec("self.config_test.SARASA = 1"))

    def test_save(self):
        """Save a new configuration and reopen the file to test saving"""
        newvalue = "libertad"

        cfg = _Config()
        self.assertNotEqual(cfg.USER_ALLOWED, newvalue)

        self.config_test.USER_ALLOWED = newvalue
        self.config_test.save()

        cfg = _Config()
        self.assertEqual(cfg.USER_ALLOWED, newvalue)

    def tearDown(self):
        """Remove fake config file"""
        if os.path.exists(config.FILEPATH):
            os.remove(config.FILEPATH)


# to allow the creation of a fake config file
parent_dir = os.path.dirname(os.path.realpath(__file__))
config.FILEPATH = os.path.join(parent_dir, "test.cfg")
_Config = config.__dict__['_Config']
