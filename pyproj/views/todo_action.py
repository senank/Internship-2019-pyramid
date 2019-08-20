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

# import colander
# from deform import Form

# class TodoForm(colander.MappingSchema):
#     # id_ = colander.SchemaNode(colander.Integer())
#     description = colander.SchemaNode(colander.String())
#     # checked = colander.SchemaNode(colander.Boolean())

# sample_data = {
#     '1': dict(id = '1', description = 'ToDoItem-1'),
#     '2': dict(id = '', description = 'ToDoItem-2')
# }


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
    return HTTPFound(location=request.route_url('todo_list'))

@view_config(route_name='todo_item_delete', request_method='POST', permission='delete')
def todo_item_delete(request):
    request.dbsession.query(TodoItem).filter_by(user_id = request.user.user_id).filter(TodoItem.completed == True).delete()
    return HTTPFound(location=request.route_url('todo_list'))
    # completed_list = request.dbsession.query(TodoItem).filter(TodoItem.completed == True)
    # for item in completed_list:
    #    item.completed = False
       #request.dbsession.delete(item)
            


@view_config(route_name='todo_item_edit', renderer='../templates/todo_edit.mako', permission='edit')
def todo_item_edit(request):
    try:
        id_ = int(request.matchdict['id'])
    except (ValueError, TypeError):
        raise HTTPNotFound

    item = request.dbsession.query(TodoItem).filter_by(user_id = request.user.user_id).filter(TodoItem.id == id_).first()
    if item is None:
        raise HTTPForbidden
    
    todos = request.dbsession.query(TodoItem).filter_by(user_id = request.user.user_id)

    submitted = request.POST.get('submitted')
    valid = True
    form_data = {}
    error = {}

    if submitted:
        try:
            description = request.POST.get('description')
            if description is not None:
                description = description.strip()
                if 0 < len(description) <= 24:
                    form_data['description'] = description
                else:
                    valid = False
                    error['description'] = 'Description field is too short or too long'
        
            position = request.POST.get('position')
            if position is not None:
                try:
                    position = int(position.strip())
                except ValueError:
                    valid = False
                    error['position'] = 'Please enter a number'
                else:
                    max_position = request.dbsession.query(func.max(TodoItem.position)).scalar() or 0
                    if 1 <= position <= max_position + 1:
                        form_data['position'] = position
                    else:
                        valid = False
                        error['position'] = 'Position is outside of the range'

            completed = request.POST.get('completed')
            if completed is not None:
                completed = completed.lower()
                if completed in ('yes', 'true', 'on', '1', 'no', 'false', 'off', '0'):
                    form_data['completed'] = completed in ('yes', 'true', 'on', '1')
                else:
                    valid = False
                    error['completed'] = 'Completed value is invalid'

        except (ValueError, TypeError, KeyError) as e:
            valid = False

    if submitted and valid and form_data:
        if 'description' in form_data:
            item.description = form_data['description']
        
        if 'position' in form_data:
            #gets number of todos that have have to be moved
            shift = item.position - (form_data['position'] - 1)

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


        if 'completed' in form_data:
            item.completed = form_data['completed']
            if item.completed:
                item.completed_date = datetime.now()
            else:
                item.completed_date = None

        request.dbsession.add(item)
        return HTTPFound(location=request.route_url('todo_list'))
    
    elif submitted:
        error['_'] = 'Please check your data'

    return {
        'error': error,
        'item': item,
        'id': id_,
        'todos' : todos
    }


db_err_msg = 'Unable to process data'

@view_config(route_name = 'todo_item_drag', permission = 'dnd', require_csrf = False)
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