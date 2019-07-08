from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..models import TodoItem

import logging
log = logging.getLogger(__name__)


@view_config(route_name='todo_item_complete')
def todo_item_complete(request):
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


@view_config(route_name='todo_item_add', request_method='POST')
def todo_item_add(request):
    item = TodoItem()
    item.description = request.params.get('description') or ''
    item.completed = False
    request.dbsession.query(func.max(TodoItem.position) + 1).filter(TodoItem.completed.is_(False))
    item.position = request.dbsession.query(func.max(TodoItem.position) + 1).filter(TodoItem.completed.is_(False)).scalar() or 0
    item.created_date = datetime.now()
    request.dbsession.add(item)
    return HTTPFound(location=request.route_url('todo_list'))


db_err_msg = 'Unable to process data'
