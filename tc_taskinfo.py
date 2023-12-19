#!/usr/bin/env python3

"""
Test cases for taskinfo.py
"""

import unittest
import shutil
import os
import taskinfo
# from mock import patch


def identify(testobj):
    """Identify running test in log"""
    print(f"\n{'='*72}\n{testobj.id().split('.')[-1]}\n{'='*72}")

# @patch('os.path.exists')
# @patch('os.makedirs')
# def test_store_symbols_create_directory_fails(
#     self, mock_makedirs, mock_path_exists):
#     mock_path_exists.return_value = False
#     mock_makedirs.side_effect = os.error
#     succeeded = self.symbol_db.store_symbols(
#             self.unstripped,
#             self.stripped
#             )
#     print "The test ran and returned {}".format(succeeded)
#     self.assertFalse(succeeded)


class TestTaskInfo(unittest.TestCase):
    """Test TaskInfo class"""
    def setUp(self):
        """Set up before test cases"""
        identify(self)
        self.task = None
        self.test_dir = os.path.realpath("./temp/")
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def tearDown(self):
        """Tear down after test cases"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_taskinfo_add_build(self):
        """Test TaskInfo creation for a Build task"""
        self.task = taskinfo.TaskInfo('Do the first thing', 'Build')
        print(f"task id = {self.task.id}")
        print(f"task type = {self.task.type}")
        self.assertEqual(self.task.description, 'Do the first thing')

    def test_taskinfo_add_test(self):
        """Test TaskInfo creation for a Test task"""
        self.task = taskinfo.TaskInfo('Do the second thing', 'Test')
        print(f"task id = {self.task.id}")
        print(f"task type = {self.task.type}")
        self.assertEqual(self.task.description, 'Do the second thing')


class TestTasksInProgress(unittest.TestCase):
    """Test TasksInProgress class"""
    def setUp(self):
        """Set up before test cases"""
        identify(self)
        self.tasks_in_progress = None
        self.test_dir = os.path.realpath("./temp/")
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def tearDown(self):
        """Tear down after test cases"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_tasks_in_progress_push(self):
        """Test TaskInfo creation for a Build task"""
        self.tasks_in_progress = taskinfo.TasksInProgress()
        types = ['build', 'test', 'mentor']
        priorities = [taskinfo.TaskPriority.MEDIUM,
                      taskinfo.TaskPriority.LOW,
                      taskinfo.TaskPriority.MEDIUM,
                      taskinfo.TaskPriority.HIGH,
                      taskinfo.TaskPriority.CRITICAL,
                      taskinfo.TaskPriority.SHOWSTOPPER,
                      taskinfo.TaskPriority.MEDIUM,
                      taskinfo.TaskPriority.HIGH,
                      taskinfo.TaskPriority.CRITICAL,
                      taskinfo.TaskPriority.SHOWSTOPPER]
        for i in range(0, 10):
            task = taskinfo.TaskInfo(f"Task #{i}", 'build')
            task.type = types[i % len(types)]
            task.set_priority(priorities[i])
            self.tasks_in_progress.push(task)
        self.tasks_in_progress.dump()


# class TestAdd(unittest.TestCase):
#     """Test the 'add' command"""
#     def setUp(self):
#         """Set up before test cases"""
#         identify(self)
#         self.test_dir = os.path.realpath("./temp/")
#         shutil.rmtree(self.test_dir, ignore_errors=True)
#
#     def tearDown(self):
#         """Tear down after test cases"""
#         shutil.rmtree(self.test_dir, ignore_errors=True)
#
#     def test_process_command_add_build(self):
#         """Test the 'add' command for a Build task"""
#         cmd_add.process_command({type: 'Build'})
#
#     def test_process_command_add_test(self):
#         """Test the 'add' command for a Test task"""
#         cmd_add.process_command({type: 'Test'})


if __name__ == '__main__':
    unittest.main()
