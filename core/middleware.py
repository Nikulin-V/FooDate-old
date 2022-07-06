from threading import current_thread

from django.utils.deprecation import MiddlewareMixin

_requests = {}


def get_user():
    thread = current_thread()
    if thread not in _requests:
        return None
    return _requests[thread].user


class RequestMiddleware(MiddlewareMixin):
    # noinspection PyMethodMayBeStatic
    def process_request(self, request):
        _requests[current_thread()] = request
