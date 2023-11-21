# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import unittest

from pygroupcache import get, set, setup, initialized


class PyGroupCacheTest(unittest.TestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        setup("localhost:15555", "http://localhost:15555")
        if initialized():
            self.initialized = True
        else:
            self.initialized = False

    def test_set_and_get_existing_or_non_existing_key(self):
        if not self.initialized:
            self.skipTest("Cache not initialized")
        key = "existing_key"
        value = "existing_value"
        set(key, value)
        ret_value = get(key)
        self.assertEqual(ret_value, value)
        key = "non_existing_key"
        ret_value = get(key)
        self.assertEqual(ret_value, "")

    def tearDown(self):
        if self.initialized:
            pass


if __name__ == "__main__":
    unittest.main()
