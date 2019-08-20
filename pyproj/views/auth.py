from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.csrf import new_csrf_token

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..security import check_password, hash_password

from ..models import User
from ..models import TodoItem

@view_config(route_name='create', renderer='../templates/create_acc.mako', request_method='GET', require_csrf=False)
def create(request):
    return {
        'project': 'To-Do',
        'page_title': 'Create'
    }

@view_config(route_name='create', renderer='../templates/create_acc.mako', request_method='POST', require_csrf=False)
def create_acc(request):
    form_data = {}
    error = {}
    forbidden = ["{","}", "|", "\'","^", "~", "[", "]", "`"]
    valid = True

    try:
        form_username = request.POST.get('username')
        if form_username:
            db_username = request.dbsession.query(User).filter(User.username == form_username).first()
            if db_username is None:
                form_data['username'] = form_username
            else:
                valid = False
                error['username_taken'] = 'That username has been taken'
        else:
            valid = False
            error['username_invalid'] = 'Please enter a valid username'
        form_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if form_password:
            if form_password == confirm_password:
                chars = True
                for char in forbidden:
                    if char in form_password:
                        error['password'] = \
                            'Please avoid the following:   {  ,  }  ,  |  ,  \'  ,  ^  ,  ~  ,  [ , ] , ` '
                        chars = False
                        valid = False
                if chars:
                    form_data['password'] = form_password
            elif form_password != confirm_password:
                error['nomatch'] = 'Password did not match'
                valid = False
        elif confirm_password:
            error['nopassword'] = 'Please enter a password'
            valid = False
        else:
            error['password'] = 'Password cannot be empty'
            valid = False
    except (ValueError, TypeError, KeyError) as e:
        valid = False
    
    if valid:
        new_user = User()
        new_user.username = form_data['username'].lower()

        password_hashed = hash_password(form_data['password'])
        new_user.password = password_hashed

        new_user.permissions = 'admin'

        request.dbsession.add(new_user)
        request.dbsession.flush()
        headers = remember(request, new_user.user_id)
        new_csrf_token(request)
        return HTTPFound(location=request.route_url('home'), headers=headers)
    else:
        return {
            'project': 'To-Do',
            'page_title': 'Create',
            'error': error,
            }

@view_config(route_name='edit_user', renderer = "../templates/edit_user.mako",\
     request_method='GET', permission = 'logged')
def edit(request):
    return {
        'project': 'To-Do',
        'page_title': 'Edit'
    }


@view_config(route_name='edit_user', renderer = "../templates/edit_user.mako", request_method='POST', permission = 'logged')
def edit_handler(request):
    form_data = {}
    error = {}
    forbidden = ["{","}", "|", "\'","^", "~", "[", "]", "`"]
    valid = True

    id_ = request.user.user_id
    user = request.dbsession.query(User).filter_by(user_id = id_).first()
    

    try:
        form_username = request.POST.get('username')
        if form_username:
            db_username = request.dbsession.query(User).filter(User.username == form_username).first()
            if db_username is None or user.username:
                form_data['username'] = form_username
            else:
                valid = False
                error['username_taken'] = 'That username has been taken'
        else:
            form_data['username'] = user.username

        form_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm')

        if form_password:
            if (form_password == confirm_password):
                chars = True    
                for char in forbidden:
                    if char in form_password:
                        error['password'] = \
                             'Please avoid the following:   {  ,  }  ,  |  ,  \'  ,  ^  ,  ~  ,  [ , ] , ` '
                        chars = False
                        valid = False
                if chars:
                    password = hash_password(form_password)
                    form_data['password'] = password
            elif (form_password != confirm_password):
                error['nomatch'] = 'Password did not match'
                valid = False
        elif confirm_password is not None:
            error['nopassword'] = 'Please enter a password'
            valid = False
        else:
            form_data['password'] = user.password
            
    except (ValueError, TypeError, KeyError):
        valid = False
    
    if valid:
        user.username = form_data['username'].lower()
        user.password = form_data['password']

        request.dbsession.add(user)
        return HTTPFound(location=request.route_url('home'))

    return {
        'project': 'To-Do',
        'page_title': 'Edit',
        'error': error,
    }


@view_config(route_name='login', renderer = "../templates/login.mako", request_method='GET', require_csrf=False)
def login(request):
    return {
        'project': 'To-Do',
        'page_title': 'Login',
    }

@view_config(route_name='login', renderer = "../templates/login.mako", request_method='POST', require_csrf=False)
def login_handler(request):
    valid = True
    error = {}

    form_username = request.POST.get('username').lower()
    form_password = request.POST.get('password')
    
    db_user = request.dbsession.query(User).filter_by(username = form_username).first()
    
    if db_user and check_password(form_password, db_user.password):
        id_ = db_user.user_id
        headers = remember(request, id_)
        new_csrf_token(request)
        return HTTPFound(location=request.route_url('home'), headers=headers)
 
    error['incorrect'] = 'Check username or password'
    return {
            'error': error,
            'page_title': 'Login',
            'project': 'To-Do',
            }

@view_config(route_name='logout', require_csrf=False)
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='delete_user', request_method='POST')
def delete_user(request):
    user = request.user
    request.dbsession.query(User).filter_by(user_id = user.user_id).delete()
    request.dbsession.query(TodoItem).filter_by(user_id = user.user_id).delete()
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
    
