import os


class AdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            os.environ['DJANGO_SETTINGS_MODULE'] = '../django_settings.admin_settings'
        else:
            os.environ['DJANGO_SETTINGS_MODULE'] = '../django_settings.settings'

        return self.get_response(request)
