from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        allowed_paths = [reverse('accounts:login'), reverse('accounts:register')]

        if not request.path_info.startswith("/admin") and not request.user.is_authenticated and request.path_info not in allowed_paths:
            return redirect('accounts:login')

        return response