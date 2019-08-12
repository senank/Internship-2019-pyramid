<%inherit file="layout.mako"/>

<h1>Create an Account! :)</h1>
<form action = "${request.route_url('create')}" method = "POST">
    <input type="text" name = "username" placeholder="Please insert a username">
    <input type = "text" name = "password" placeholder = "Please insert a password">
    <input name = 'login_submit' type = "submit" class = "btn btn-danger">
</form>
%if error:
    %for key, msg in error.items():
        <p class="alert alert-danger">
            ${msg}
        </p>
    %endfor
%endif