from django.shortcuts import redirect
from django.urls import reverse

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica si el usuario está autenticado
        logueo = request.session.get("logueo")
        if logueo:
            request.user_role = logueo.get("rol", None)
        else:
            request.user_role = None

        response = self.get_response(request)

        return response
