<%inherit file="layout.mako"/>
<div class="content">

   <h1>To-Do</h1>

<p>Allowed: ${'${}'}</p>

   <ul>
   % for item in todos:
      <li>
         <input type="checkbox" value="1" name="todo-${item.id}" data-id="${item.id}"
            % if item.completed:
                checked
            % endif
         >
         ${item.description}
         % if item.completed:
             at ${item.completed_date}
         % endif
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


<%block name="page_script">
<script>

jQuery(function($){
    $(document).on('change', 'input[name^="todo-"]', function(){
        $.post('${request.route_url('todo_item_complete')}', {id: $(this).data('id'), checked: $(this).is(':checked')});
    });
});

</script>
</%block>
