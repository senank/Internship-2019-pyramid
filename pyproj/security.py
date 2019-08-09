from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import User

class MyAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.id

def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        user = request.dbsession.query(User).get(user_id)
        return user

def groupfinder(userid, request):
    user = get_user()
    permissions = []
    if user is not None:
        for permission in user.permissions.split(','):
            permissions.append(permission)
    return permissions



def includeme(config):
    settings = config.get_settings()
    authn_policy = AuthTktAuthenticationPolicy(
            settings['pyproj.secret'], callback = groupfinder,
            hashalg='sha512'
    )
    authz_policy=ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_request_method(get_user, 'user', reify=True)