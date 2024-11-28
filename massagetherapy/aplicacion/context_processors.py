def rol_context_processor(request):
    logueo = request.session.get("logueo", {})
    return {'rol': logueo.get("rol", None)}
