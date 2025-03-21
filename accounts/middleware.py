from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import logout

class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.session_key and request.user.session_key != request.session.session_key:
                logout(request)
                return redirect(settings.LOGIN_URL)
            
        response = self.get_response(request)
        return response