from pyramid.view import view_config
from pyramid.response import Response
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..models import User

@view_config(route_name='login', renderer = "../templates/login.mako", request_method='GET')
def login(request):
    pass

@view_config(route_name='login', renderer = "../templates/login.mako", request_method='POST')
def login_handler(request):
    submitted = request.POST.get('login_submit')
    valid = True
    form_data = {}
    error = {}
    forbidden = ["{","}", "|", "\'","^", "~", "[", "]", "`"]
    if submitted:
        try:
            username = request.POST.get('username')
            if username is not None:
                form_data['username'] = username
            else:
                valid = False
                error['username'] = 'There is no existing user with that username'
            password = request.POST.get('password')
            if password is not None:
                chars = True
                for char in forbidden:
                    if char in password:
                        error['password'] = 'Please check password'
                        chars = False
                        valid = False
                if chars:
                    form_data['password'] = password
            else:
                error['password'] = 'Please check password'
        except (ValueError, TypeError, KeyError) as e:
            valid = False

    if submitted and valid and form_data:
        headers = remember(request, form_data['username'])
    
    if submitted:
        error['_'] = 'Please check your data'

    return {
        'error': error,
        'page_title': 'Login',
        'project': 'To-Do',
    }

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return Response('Logged out', headers=headers)