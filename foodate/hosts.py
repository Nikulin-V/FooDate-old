from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'', 'app.urls', name='app'),
    host(r'm', 'app_mobile.urls', name='app_mobile'),
    host(r'book', 'book.urls', name='book')
)
