import json
import time
from datetime import datetime

from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory

from tasks.models import Task

from .views import TasksApiView


class TestTasksApiView(TestCase):
    def setUp(self):
        self.task = Task.objects.create(start_time=datetime.fromtimestamp(time.time()),
                                        status=Task.COMPLETED,
                                        time_to_execute=0)
        self.task.start_time = datetime.fromtimestamp(time.time())

        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get('api/v.0.0.1/json/tasks?id=%d' % self.task.id)
        response = TasksApiView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        obj_dict = json.loads(response.content)
        self.assertEqual(obj_dict['status'], self.task.status)
        self.assertEqual(obj_dict['time_to_execute'], self.task.time_to_execute)
        self.assertIsNotNone(obj_dict['create_time'])
        self.assertIsNotNone(obj_dict['start_time'])

        request = self.factory.get('api/v.0.0.1/json/tasks?id=%d' % (self.task.id + 1))
        self.assertRaises(Http404, TasksApiView.as_view(), request)

    def test_post(self):
        request = self.factory.post('api/v.0.0.1/json/tasks')
        response = TasksApiView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        obj_dict = json.loads(response.content)
        self.assertEqual(obj_dict['id'], self.task.id + 1)

    def test__get_obj_dict(self):
        obj_dict = TasksApiView._get_obj_dict(self.task, ('id', 'status', 'not_field'))
        self.assertEqual(obj_dict['id'], self.task.id)
        self.assertEqual(obj_dict['status'], self.task.status)
        self.assertEqual(obj_dict.get('not_field', 'keyerror'), 'keyerror')
