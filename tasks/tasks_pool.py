from queue import Queue, Empty
from threading import Thread

from django.conf import settings


class TasksPool:
    def __init__(self):
        self._queue = Queue()
        self._workers = [Thread(target=self._run)
                         for _ in range(settings.THREADS_MAX_COUNT)]
        self._start_workers()

    def add(self, task):
        self._queue.put(task)
        task.set_pending()

    def _run(self):
        while True:
            try:
                task = self._queue.get()
            except Empty:
                pass
            else:
                task.run()
                self._queue.task_done()

    def _start_workers(self):
        for worker in self._workers:
            worker.start()


tasks_pool = TasksPool()
