from django.http import HttpResponseRedirect


def pc_redirect(redirect_url):
    """Redirects to pc version of page"""
    def pc_redirect_decorator(func):
        def _wrapper(*args, **kwargs):
            request = args[1]
            if request.user_agent.is_pc:
                return HttpResponseRedirect(redirect_url)
            return func(*args, **kwargs)
        return _wrapper
    return pc_redirect_decorator


def mobile_redirect(redirect_url):
    """Redirects to mobile version of page"""
    def mobile_redirect_decorator(func):
        def _wrapper(*args, **kwargs):
            request = args[1]
            if request.user_agent.is_mobile or request.user_agent.is_tablet:
                return HttpResponseRedirect(redirect_url)
            return func(*args, **kwargs)
        return _wrapper
    return mobile_redirect_decorator
