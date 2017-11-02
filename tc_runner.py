#!/usr/bin/env python

import unittest
import runner


def identify(testobj):
    print("\n{}\n{}\n{}".format("="*72, testobj.id().split('.')[-1], "="*72))
    return


class TestRunCommand(unittest.TestCase):
    def setUp(self):
        identify(self)

    def test_run_command(self):
        status, output, errors = runner.run_command(["ls", "-alt"])
        status, output, errors = runner.run_long_command(["ls", "-alt"])


if __name__ == '__main__':
    unittest.main()
