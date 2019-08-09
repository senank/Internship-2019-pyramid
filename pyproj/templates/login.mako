<%inherit file="layout.mako"/>
<div class="content">

    <h1>Login</h1>
%if error:
    %for key, msg in error.items():
        <p class="alert alert-danger">
            ${msg}
        </p>
    %endfor
%endif

<form action = "${request.route_url('login')}" method = "POST">
    <input type="text" name = "username" placeholder="username">
    <input type = "text" name = "password" placeholder = "password">
    <input name = 'login_submit' type = "submit" class = "btn btn-danger">
</form>
</div>