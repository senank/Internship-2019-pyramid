def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('todo_list', '/todo')
    config.add_route('todo_item_complete', '/todo/complete')
    config.add_route('todo_item_add', '/todo/new')
    config.add_route('todo_item_delete', '/todo/delete')
    config.add_route('todo_item_edit', '/todo/edit/{id}')
    config.add_route('todo_item_drag', '/todo/dnd')
    