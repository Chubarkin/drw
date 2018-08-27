from django.views.generic import View
from django.http import JsonResponse, Http404

from tasks.models import Task
from tasks.tasks_pool import tasks_pool


class TasksApiView(View):
    def get(self, request):
        task_id = request.GET.get('id')
        task = Task.objects.filter(pk=task_id).first()
        if not task:
            raise Http404()

        obj_dict = self._get_obj_dict(task, (
            'status', 'create_time', 'start_time', 'time_to_execute'))
        return JsonResponse(obj_dict)

    def post(self, request):
        task = Task.objects.create()
        tasks_pool.add(task)

        obj_dict = self._get_obj_dict(task, ('id',))
        return JsonResponse(obj_dict)

    @staticmethod
    def _get_obj_dict(obj, fields):
        return {field: obj.__dict__[field]
                for field in fields if hasattr(obj, field)}
