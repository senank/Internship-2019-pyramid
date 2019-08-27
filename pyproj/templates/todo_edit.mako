<%inherit file="layout.mako"/>
<% filepath = 'pyproj:static/uploads/' + item.unique_filename %>
<h1>
    %if 'image' in item.mimetype:
        <img src="${request.static_url(filepath)}" height = "128" width = "128">
    %else:
        <i class="${item.get_icon()}"></i>
    %endif
    ${desc} 
</h1>
## % if error:
##     % for key, msg in error.items():
##         <p class="alert alert-danger">
##            % if key == '_':
##                ${error}
##            % else:
                ## ${msg}
##            % endif
        ## </p>
##     % endfor
## % endif
<p><a href="${request.static_url(filepath)}"><i class="fa fa-download"></i> ${item.filename} <i class="${item.get_icon()}"></i></a></p>


## <form action="${request.route_url('todo_item_edit', id=item.id)}" name="editting" id="editting" method="POST">
##     <div class = "form-group">
##         <input id="description" class = "form-control" type='text' name="description" value="${item.description}">
##     </div>
##     <div class = "form-group">
##         <label>Position
##             <select name='position' class="custom-select custom-select-lg">
##                 %for x in todos:    
##                     %if item.id == x.id:
##                         <option selected hidden>${x.position+1}</option>
##                     %endif
##                 %endfor
##                 <% 
##                 count = 0
##                 for x in todos:
##                     count += 1
##                 %>
##                 %for x in range(count):
##                     <option>${x+1}</option>
##                 %endfor
                
##             </select>
##         </label>
##         <label>Completed
##             <select name='completed'>
##                 % if item.completed:        
##                     <option value="yes" selected>Yes</option>
##                     <option value="no">No<option>
##                 % elif not item.completed:
##                     <option value="yes">Yes</option>
##                     <option value="no" selected>No<option>
##                 %endif
##             </select>
##         </label>
##     </div>
##     <div>
##         <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
##         <input type='submit' class='btn btn-default' name='submitted' value='yes'>
##     </div>
## </form>
${form | n}

##<a href="${request....}">
##    <i class="${item.get_icon()}"></i> ${filename}
##</a>

##
##<script>
##    jQuery(function($){
##    var opt = $("position option").sort(function (a,b) { return a.value.toUpperCase().localeCompare(b.value.toUpperCase()) });
##    $("#position").append(opt);
##    $("#position").find('option:first').attr('selected','selected');
##});
##</script>