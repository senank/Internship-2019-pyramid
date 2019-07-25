<%inherit file="layout.mako"/>
<h1>Editting: ${item.description}</h1>
% if error:
    % for key, msg in error.items():
        <p class="alert alert-danger">
            % if key == '_':
                ${error}
            % else:
                ${key}: ${error}
            % endfor
        </p>
    % endfor
% endif
<form action="${request.route_url('todo_item_edit', id=item.id)}" name="editting" id="editting" method="POST">
    <div>
        <input id="description" type='text' name="description" value="${item.description}">
    </div>
    <div>
        <label>Position
            <select name='position'>
                ##<option disabled selected hidden>${item.position+1}</option>
                %for x in todos:
                    %if item.id == x.id:
                        <option selected hidden>${x.position+1}</option>
                    %endif
                    <option>${x.id}</option>
                %endfor
            </select>
        </label>
        <label>Completed
            <select name='completed'>
                <option value="yes"
                    % if item.completed:
                    selected
                    % endif
                >Yes<option>
                <option value="no"
                    % if not item.completed:
                    selected
                    % endif
                >No<option>
            </select>
            ##<input type='checkbox' name='completed'
            ##    % if item.completed:
            ##        checked
            ##    % endif
            ##>
        </label>
    </div>
   
    <input type='submit' class='btn btn-default' name='submitted' value='yes'>
</form>
<a href="${request.route_url('todo_list')}">Home</a>

##<script>
##    jQuery(function($){
##        $("#editting").submit(function(event){
##            var description = $('#description').val();
##            $.post("${request.route_url('todo_item_edit', id=item.id)}", {description: description, submitted: 'yes'}, function(data))
##        });
##    });
##</script>