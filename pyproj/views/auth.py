from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..models import User

@view_config(route_name='create', renderer='../templates/create_acc.mako', request_method='GET')
def create(request):
    return {
        'project': 'To-Do',
        'page_title': 'Create'
    }

@view_config(route_name='create', renderer='../templates/create_acc.mako', request_method='POST')
def create_acc(request):
    form_data = {}
    error = {}
    forbidden = ["{","}", "|", "\'","^", "~", "[", "]", "`"]
    valid = True

    try:
        form_username = request.POST.get('username')
        if form_username:
            # try:
            db_username = request.dbsession.query(User).filter(User.username == form_username).first()
            if db_username is None:
                form_data['username'] = form_username
            else:
                valid = False
                error['username_taken'] = 'That username has been taken'
            
            # except DBAPIError as e:
                # log.exception(e)
                # valid = False
        else:
            valid = False
            error['username_invalid'] = 'Please enter a valid username'
        form_password = request.POST.get('password')
        if form_password:
            chars = True
            for char in forbidden:
                if char in form_password:
                    error['password'] = 'Please avoid the following:   {  ,  }  ,  |  ,  \'  ,  ^  ,  ~  ,  [ , ] , ` '
                    chars = False
                    valid = False
            if chars:
                form_data['password'] = form_password
        else:
            error['password'] = 'Please enter a valid password'
            valid = False
    except (ValueError, TypeError, KeyError) as e:
        valid = False
    
    if valid:
        new_user = User()
        new_user.username = form_data['username']
        new_user.password = form_data['password']
        request.dbsession.add(new_user)
        request.dbsession.flush()
        headers = remember(request, new_user.user_id)
        return HTTPFound(location=request.route_url('home'), headers=headers)
    else:
        return {
            'project': 'To-Do',
            'page_title': 'Create',
            'error': error,
            }
    

@view_config(route_name='login', renderer = "../templates/login.mako", request_method='GET')
def login(request):
    return {
        'project': 'To-Do',
        'page_title': 'Login',
    }

@view_config(route_name='login', renderer = "../templates/login.mako", request_method='POST')
def login_handler(request):
    valid = True
    error = {}
    form_username = request.POST.get('username')
    form_password = request.POST.get('password')
    
    db_user = request.dbsession.query(User).filter_by(username = form_username).first()
    if db_user and db_user.password == form_password:
        id_ = db_user.user_id
        headers = remember(request, id_)
        return HTTPFound(location=request.route_url('home'), headers=headers)
 
    error['incorrect'] = 'Check username or password'
    return {
            'error': error,
            'page_title': 'Login',
            'project': 'To-Do',
            }

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)