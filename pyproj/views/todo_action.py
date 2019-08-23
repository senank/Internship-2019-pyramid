from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.csrf import get_csrf_token
import pyramid.events

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..models import TodoItem

import logging
log = logging.getLogger(__name__)

import colander
import deform

@colander.deferred
def deferred_csrf_default(node, kw):
    request = kw.get('request')
    csrf_token = request.session.get_csrf_token()
    return csrf_token

@view_config(route_name='todo_item_complete', permission = 'complete')
def todo_item_complete(request):
    
    item = None
    try:
        if request.params.get('id') is not None:
            item = request.dbsession.query(TodoItem).get(request.params['id'])
    except DBAPIError as ex:
        log.exception(ex)
        return Response(db_err_msg, content_type='text/plain', status=500)


    if item:
        completed = request.params.get('checked') == 'true'
        item.completed = completed
        if completed:
            item.completed_date = datetime.now()
        request.dbsession.add(item)
    else:
        return Response('Not Found', content_type='text/plain', status=404)

    return Response('OK', content_type='text/plain', status=200)


@view_config(route_name='todo_item_add', request_method='POST', permission='add')
def todo_item_add(request):
    
    todos = request.dbsession.query(TodoItem).filter_by(user_id = request.user.user_id)
    
    count = 0
    for item in todos:
        count += 1

    item = TodoItem()
    item.description = request.params.get('description') or ''
    item.completed = False
    item.position = count
    item.created_date = datetime.now()
    item.user_id = request.user.user_id
    request.dbsession.add(item)
    
@view_config(route_name='todo_item_delete', request_method='POST', permission='delete')
def todo_item_delete(request):
    
    request.dbsession.query(TodoItem).filter_by(user_id = \
        request.user.user_id).filter(TodoItem.completed == True).delete()



@view_config(route_name='todo_item_edit', renderer='../templates/todo_edit.mako', permission='edit')
def todo_item_edit(request):
    try:
        id_ = int(request.matchdict['id'])
    except (ValueError, TypeError):
        raise HTTPNotFound

    item = request.dbsession.query(TodoItem).filter_by(user_id = \
        request.user.user_id).filter(TodoItem.id == id_).first()
        
    if item is None:
        raise HTTPForbidden
    
    todos = request.dbsession.query(TodoItem).filter_by(user_id = request.user.user_id)
    
    #position list for select
    position_list = ()
    count = 0
    for x in todos:
        count += 1
        position_list += ((count, count,),)

    #for default values
    current = {
        'description' : item.description,
        'position' : item.position + 1,
        'completed' : item.completed
    }
    
    #form with CSRF
    schema = colander.SchemaNode(colander.Mapping(), 
        colander.SchemaNode(colander.String(), 
        name = 'csrf_token',
        default=deferred_csrf_default,
        widget=deform.widget.HiddenWidget(),
        ).bind(request=request))

    #description
    schema.add(colander.SchemaNode(colander.String(),
        validator = colander.Length(min = 1, max = 24),
        description = 'New name',
        name = 'description',
        default = current['description']))

    #position
    schema.add(colander.SchemaNode(colander.Integer(),
        validator = colander.Range(min = 1, max = count),
        widget = deform.widget.SelectWidget(values=position_list),
        description = 'Select position',
        name = 'position',
        default = current['position']))
    
    #completed
    schema.add(colander.SchemaNode(colander.Boolean(),
        #validator = colander.OneOf([True, False]),
        widget = deform.widget.SelectWidget(values=(('true', 'Yes',),('false',' No',))),
        description = 'Finished',
        name = 'completed',
        default = current['completed']))

    myform = deform.Form(schema, buttons = ('submit', 'cancel',))
    form = myform.render()

    if 'submit' in request.POST:
        control = request.POST.items()
        
        try:
            form_data = myform.validate(control)
        except deform.exception.ValidationFailure as e:
            return {
                'todos': todos,
                'page_title': 'To-Do',
                'project': 'To-Do',
                'form': e.render(),
                'desc': current['description']
                }


        item.description = form_data['description']

        shift = item.position - (form_data['position']-1)        
        while shift < 0: #moving up position
            curr = item.position
            for x in todos:
                if x.position == curr + 1:
                    x.position = curr
                    item.position = curr + 1
                    curr += 1
                    shift += 1
                    request.dbsession.add(x)

        while shift > 0: #moving down position
            curr = item.position
            for x in todos:
                if x.position == curr - 1:
                    x.position = curr
                    item.position = curr - 1
                    curr -= 1
                    shift -= 1
                    request.dbsession.add(x)


        item.completed = form_data['completed']
        if item.completed:
            item.completed_date = datetime.now()
        else:
            item.completed_date = None

        request.dbsession.add(item)
        return HTTPFound(location=request.route_url('todo_list'))
    
    elif 'cancel' in request.POST:
        return HTTPFound(request.route_url('todo_list'))

   
    return {
        'item': item,
        'id': id_,
        'todos' : todos,
        'form' : form,
        'desc': current['description']
    }


db_err_msg = 'Unable to process data'

@view_config(route_name = 'todo_item_drag', permission = 'dnd')
def todo_item_drag(request):
    data = {}
    for key, value in request.POST.items():
        if not key.startswith('id-'):
            continue
        _, key = key.split('-', 1)
        try:
            data[int(key)] = int(value)
        except ValueError:
            return Response(db_err_msg, content_type='text/plain', status=500)

    if not data:
        return Response(db_err_msg, content_type='text/plain', status=500)

    todos = request.dbsession.query(TodoItem).filter(TodoItem.id.in_(data.keys()))
    for item in todos:
        if item.id in data:
            item.position = data[item.id]
            request.dbsession.add(item)
    return Response('OK', content_type='text/plain', status=200)