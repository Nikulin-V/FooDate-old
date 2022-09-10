from django.http import HttpResponse
from django.views.decorators.http import require_GET

from foodate.settings import SCHEME


@require_GET
def robots_txt(request):
    host = request.get_host()
    lines = [
        'User-agent: *',
        'Disallow: /css',
        'Disallow: /js',
        'Disallow: /admin/',
        f'Host: {host}',
        f'Sitemap: {SCHEME}://{host}/sitemap.xml'
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
