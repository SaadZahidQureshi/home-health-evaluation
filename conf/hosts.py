from django_hosts import patterns, host
from django.conf import settings


host_patterns = patterns('',
    host(r'', 'web.urls_public', name='public'),
    host(rf'{settings.ADMIN_SUBDOMAIN}', 'web.urls_admin', name='admin'),
)
