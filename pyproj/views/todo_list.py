from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPForbidden

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..models import TodoItem

import logging
log = logging.getLogger(__name__)


@view_config(route_name='todo_list', renderer='../templates/todo_list.mako', permission = 'view')
def todo_list(request):
    #log.error(repr(dir(request.dbsession)))
    
    user = request.user
    if user is not None:
        try:
            id_ = user.user_id
            query = request.dbsession.query(TodoItem)
            todos = query.filter_by(user_id = id_).order_by(TodoItem.completed.asc(), TodoItem.position.asc()).all()
        except DBAPIError as ex:
            log.exception(ex)
            return Response(db_err_msg, content_type='text/plain', status=500)
        
    else:
        raise HTTPForbidden
    #q = request.dbsession.query(func.max(TodoItem.position) + 1).filter(TodoItem.completed.is_(False))
    #log.error(q.first())
    #log.error(q.scalar())

    return {
       'todos': todos,
       'page_title': 'To-Do',
       'project': 'To-Do',
    }


db_err_msg = 'Unable to load data'
