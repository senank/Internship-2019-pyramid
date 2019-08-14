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
        <form action = "${request.route_url('edit_user')}" method = "POST" onsubmit = "return confirm('Are you sure you want to update?')">
            <input type="text" name = "username" placeholder="new username">
            <input type = "text" name = "password" placeholder = "new password">
            <input name = 'login_submit' type = "submit" class = "btn btn-default">
        </form>

        <form action="${request.route_url('delete_user')}" method='POST' class="inline-block">
            <input name="Delete" type="submit" class="btn btn-danger" value="Delete" onclick = "return confirm('THIS WILL DELETE YOUR ACCOUNT ARE YOU SURE YOU WANT TO CONTINUE?')">
        </form>
    </div>
</div>

<a href="${request.route_url('home')}">Cancel</a>
