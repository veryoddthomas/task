#!/usr/bin/env python

import unittest
import shutil
import os
import cmd_add
# from mock import patch


def identify(testobj):
    print("\n{}\n{}\n{}".format("="*72, testobj.id().split('.')[-1], "="*72))
    return

# @patch('os.path.exists')
# @patch('os.makedirs')
# def test_store_symbols_create_directory_fails(self, mock_makedirs, mock_path_exists):
#     mock_path_exists.return_value = False
#     mock_makedirs.side_effect = os.error
#     succeeded = self.symbol_db.store_symbols(
#             self.unstripped,
#             self.stripped
#             )
#     print "The test ran and returned {}".format(succeeded)
#     self.assertFalse(succeeded)


class TestAdd(unittest.TestCase):
    def setUp(self):
        identify(self)
        self.task = None
        self.test_dir = os.path.realpath("./temp/")
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_add_1(self):
        self.task = cmd_add.Task('Build')
        print("task id = {}".format(self.task.id))
        print("task type = {}".format(self.task.type))
        #self.assertEqual(0, self.task.id)

    def test_add_2(self):
        self.task = cmd_add.Task('Test')
        print("task id = {}".format(self.task.id))
        print("task type = {}".format(self.task.type))
        #self.assertEqual(1, self.task.id)


if __name__ == '__main__':
    unittest.main()
