from django.conf import settings


def api_base_url(request):
    return { 'API_BASE_URL': settings.API_BASE_URL }


def admin_base_url(request):
    return { 'ADMIN_BASE_URL': settings.ADMIN_BASE_URL }