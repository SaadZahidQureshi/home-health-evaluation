from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'abc', 'web.urls_public', name='public'),
    host(r'admin', 'web.urls_admin', name='admin'),
)
