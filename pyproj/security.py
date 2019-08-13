from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import User

class MyAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.user_id

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

def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')

def check_password(pw, hashed_pw):
    expected_hash = hashed_pw.encode('utf8')
    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)



def includeme(config):
    settings = config.get_settings()
    authn_policy = MyAuthenticationPolicy(
            settings['pyproj.secret'], callback = groupfinder,
            hashalg='sha512'
    )
    authz_policy=ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_request_method(get_user, 'user', reify=True)