from django.shortcuts import render


# noinspection PyUnusedLocal
def bad_request(request, exception):
    return render(request, 'error_pages/400.html', status=400)


# noinspection PyUnusedLocal
def forbidden(request, exception):
    return render(request, 'error_pages/403.html', status=403)


# noinspection PyUnusedLocal
def not_found(request, exception):
    return render(request, 'error_pages/404.html', status=404)


# noinspection PyUnusedLocal
def internal_server_error(request):
    return render(request, 'error_pages/500.html', status=500)
