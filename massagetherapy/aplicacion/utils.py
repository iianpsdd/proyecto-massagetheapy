from __future__ import unicode_literals
from django.db import IntegrityError
from rest_framework.views import Response, exception_handler
from rest_framework import status
from django.http import HttpResponseForbidden

def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_role = request.session.get("logueo", {}).get("rol", None)
            if user_role not in allowed_roles:
                return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    # if there is an IntegrityError and the error response hasn't already been generated
    if isinstance(exc, IntegrityError) and not response:
        response = Response(
            {
                'message': f'Error: {exc}'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return response