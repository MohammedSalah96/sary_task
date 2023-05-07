from threading import current_thread

_requests = {}


def get_current_request():
    """
    Returns the current request (or None)
    """
    thread_id = current_thread().ident
    return _requests.get(thread_id, None)


def get_current_user():
    """
    Returns the current user (or None) extracted from the current request.
    """
    current_request = get_current_request()
    if current_request and current_request.user.is_authenticated:
        return current_request.user


class GlobalRequestMiddleware(object):
    """
    Middleware that stores the current request to be used from any part of the code.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # store request related to this thread id
        thread_id = current_thread().ident
        _requests[thread_id] = request

        # call the next middleware/view
        response = self.get_response(request)

        # clenaup
        del(_requests[thread_id])

        return response