from pyramid.view import notfound_view_config, forbidden_view_config
from pyramid.response import Response


@notfound_view_config(renderer='../templates/404.mako')
def notfound_view(request):
    request.response.status = 404
    return {}

@forbidden_view_config(renderer='../templates/403.mako')
def forbidden_view(request):
    request.response.status = 403
    return {}