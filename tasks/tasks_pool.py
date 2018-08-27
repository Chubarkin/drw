from django.conf import settings
from queue import Queue, Empty
from threading import Thread, Semaphore


class TasksPool:
    def __init__(self):
        self._queue = Queue()
        self._lock = Semaphore(settings.MAX_RUNNING_THREADS)

    def add(self, task):
        self._queue.put(task)
        task.set_in_queue()
        self._start_thread()

    def _run(self):
        with self._lock:
            try:
                task = self._queue.get(False)
            except Empty:
                pass
            else:
                task.run()
                self._queue.task_done()

    def _start_thread(self):
        thread = Thread(target=self._run)
        thread.start()


tasks_pool = TasksPool()
