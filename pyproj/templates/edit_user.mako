<%inherit file="layout.mako"/>

<div class="content">
    <h1>Edit ${request.user.username.capitalize()}</h1>
    %if error:
        %for key, msg in error.items():
            <p class="alert alert-danger">
                ${msg}
            </p>
        %endfor
    %endif
    <div class="form-group">
        <form action = "${request.route_url('edit_user')}" method = "POST" class = "inline-block" \
        onsubmit = "return confirm('Are you sure you want to update?\n\nIf field is left empty, there will be no changes made to that field')">
            <div>
                <label>Username:
                    <input type="text" class='form-control' name = "username" placeholder="${request.user.username.capitalize()}">
                </label>
            </div>
            
            <div class='form-group'>
                <label>Password:
                    <input type = "text" class='form-control' name = "password" placeholder = "password">
                </label>
                <label>Confirm:
                    <input type = "text" class='form-control' name = "confirm_password" placeholder = "confirm">
                </label>
            </div>
            <div>
                <div class='form-group'>
                    <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
                    ## <div style="float:left">
                    <input name = 'login_submit' type = "submit" class = "btn btn-primary">
                    ## </div>
                    ## <div style='float:right'>
                    <input name="Delete" id='delete' formaction = "${request.route_url('delete_user')}" type="submit" class="btn btn-danger" \
                    value="Delete ${request.user.username.capitalize()}" onclick = "return confirm('THIS WILL DELETE YOUR ACCOUNT ARE YOU SURE YOU WANT TO CONTINUE?');">
                    ## </div>
                </div>
            </div>
        </form>
    </div>
</div>
<div style='float:left; clear:left;'>
    <a href="${request.route_url('home')}">Cancel</a></br>
</div>
