from django.shortcuts import redirect
from django.urls import reverse

class AdminRememberMeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if user is on home page and has remember me cookie
        if (request.path == '/' and 
            request.COOKIES.get('admin_remembered') == 'true' and
            request.user.is_authenticated and 
            request.user.is_staff):
            return redirect('shop:admin_dashboard')
        
        response = self.get_response(request)
        return response