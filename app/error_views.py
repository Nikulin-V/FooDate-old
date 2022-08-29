from django.shortcuts import render


# noinspection PyUnusedLocal
def bad_request(request, exception):
    """View of error 400"""
    return render(request, 'error_pages/400.html', status=400)


# noinspection PyUnusedLocal
def forbidden(request, exception):
    """View of error 403"""
    return render(request, 'error_pages/403.html', status=403)


# noinspection PyUnusedLocal
def not_found(request, exception):
    """View of error 404"""
    return render(request, 'error_pages/404.html', status=404)


# noinspection PyUnusedLocal
def internal_server_error(request):
    """View of error 500"""
    return render(request, 'error_pages/500.html', status=500)
