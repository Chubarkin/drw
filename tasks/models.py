import time
from datetime import datetime
from django.conf import settings
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

    def set_in_queue(self):
        self.status = Task.IN_QUEUE
        self.save()

    def set_run(self):
        start_time = time.time()
        self.start_time = datetime.fromtimestamp(start_time)
        self.status = Task.RUN
        self.save()

    def set_completed(self):
        end_time = time.time()
        self.time_to_execute = end_time - self.start_time.timestamp()
        self.status = Task.COMPLETED
        self.save()

    def run(self):
        try:
            self._run_script(settings.SCRIPT_PATH)
        except FileNotFoundError:
            pass

    def _run_script(self, file_path):
        with open(file_path) as f:
            self.set_run()

            exec(f.read())

            self.set_completed()
