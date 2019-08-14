from pyramid.security import Allow, Everyone

class Root(object):
    __acl__ = [(Allow, 'admin', 'edit'),
               (Allow, 'admin', 'add'),
               (Allow, 'admin', 'complete'),
               (Allow, 'admin', 'dnd'),
               (Allow, 'admin', 'user')]
               

    def __init__(self, request):
        pass