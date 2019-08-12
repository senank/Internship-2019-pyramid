<%inherit file="layout.mako"/>
<div class="content">

   <h1>To-Do</h1>

<p>Allowed: ${'${}'}</p>

   <ul class='drag-events' data-update-url="${request.route_url('todo_item_drag')}">
   % for item in todos:
      <li class="slide">
         <input type="checkbox" value="1" name="todo-${item.id}" data-id="${item.id}"
            % if item.completed:
                checked
            % endif
         >
         ${item.description}
         % if item.completed:
             at ${item.completed_date}
         % endif
        <a href="${request.route_url('todo_item_edit', id=item.id)}">edit</a>
      </li>
   % endfor
   </ul>


</div>


<form action="${request.route_url('todo_item_add')}" method="POST" class="form-inline">
    <div class="form-group">
       <input name="description" type="text" class="form-control">
    </div>

    <div class="form-group">
        <input name="Add" type="submit" class="btn btn-primary">
    </div>
</form>

<form action="${request.route_url('todo_item_delete')}" method='POST' class="inline-block">
    <div class="form-group">
        <input name="Delete" type="submit" class="btn btn-danger" value="Delete">
    </div>
</form>

<%block name="page_script">
<script>

jQuery(function($){
    $(document).on('change', 'input[name^="todo-"]', function(){
        $.post("${request.route_url('todo_item_complete')}", {id: $(this).data('id'), checked: $(this).is(':checked')});
    });
});

</script>
<script type="text/javascript" src="../static/dragndrop.js"></script>
</%block>