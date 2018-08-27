import time
from datetime import datetime
from django.test import TestCase
from unittest import mock

from .models import Task
from .tasks_pool import TasksPool


class TestTask(TestCase):
    def setUp(self):
        self.task = Task()

    def test_set_in_queue(self):
        self.task.set_in_queue()
        self.assertEqual(self.task.status, Task.IN_QUEUE)

    def test_set_run(self):
        self.task.set_run()
        self.assertEqual(self.task.status, Task.RUN)
        self.assertIsNotNone(self.task.start_time)

    def test_set_completed(self):
        self.task.start_time = datetime.fromtimestamp(time.time())
        self.task.set_completed()
        self.assertEqual(self.task.status, Task.COMPLETED)
        self.assertIsNotNone(self.task.time_to_execute)

    @mock.patch('tasks.models.Task._run_script')
    def test_run(self, _run_script):
        self.task.run()
        self.assertEqual(_run_script.call_count, 1)


class TestTasksPool(TestCase):
    def setUp(self):
        self.task = Task()
        self.tasks_pool = TasksPool()

    @mock.patch('queue.Queue.put')
    @mock.patch('tasks.models.Task.set_in_queue')
    @mock.patch('tasks.tasks_pool.TasksPool._start_thread')
    def test_add(self, _start_thread, set_pending, put):
        self.tasks_pool.add(self.task)
        self.assertEqual(_start_thread.call_count, 1)
        self.assertEqual(set_pending.call_count, 1)
        self.assertEqual(put.call_count, 1)

    @mock.patch('queue.Queue.get')
    @mock.patch('queue.Queue.task_done')
    @mock.patch('tasks.models.Task.run')
    def test__run(self, run, task_done, get):
        get.return_value = self.task
        self.tasks_pool._run()
        self.assertEqual(get.call_count, 1)
        self.assertEqual(task_done.call_count, 1)
        self.assertEqual(run.call_count, 1)

    @mock.patch('threading.Thread.start')
    def test__start_thread(self, start):
        self.tasks_pool._start_thread()
        self.assertEqual(start.call_count, 1)
