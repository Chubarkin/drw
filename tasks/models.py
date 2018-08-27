import time
from datetime import datetime

from django.db import models


class Task(models.Model):
    IN_QUEUE = 'In Queue'
    RUN = 'Run'
    COMPLETED = 'Completed'

    STATUS_CHOICES = (
        (IN_QUEUE, IN_QUEUE),
        (RUN, RUN),
        (COMPLETED, COMPLETED)
    )

    status = models.CharField(null=True, choices=STATUS_CHOICES, max_length=10)
    create_time = models.TimeField(null=True, auto_now_add=True)
    start_time = models.TimeField(null=True)
    time_to_execute = models.FloatField(null=True)

    def set_pending(self):
        self.status = Task.IN_QUEUE
        self.save()

    def run(self):
        try:
            self._process_file('tasks/test.py')
        except FileNotFoundError:
            pass

    def _process_file(self, file_path):
        with open(file_path) as f:
            start_time = time.time()
            self.status = Task.RUN
            self.start_time = datetime.fromtimestamp(start_time)
            self.save()

            exec(f.read())

            end_time = time.time()
            self.time_to_execute = end_time - start_time
            self.status = Task.COMPLETED
            self.save()
