<%inherit file="layout.mako"/>

<h1>Create an Account! :)</h1>
<form action = "${request.route_url('create')}" method = "POST">
    <div class = 'form-group'>
        <div>
            <label>Username:
                <input type="text" class = 'form-control' name = "username" placeholder = 'username' required>
            </label>
        </div>
        <div>
            <label>Password:
                <input type = "password" class = 'form-control' name = "password" placeholder = 'Password'required>
            </label>
            <label>Confirm:
                <input type = 'password' class = 'form-control' name ="confirm_password" placeholder = 'Confirm' required>
            </label>
        </div>
    </div>
    <div class='form-group'>
        <input name = 'login_submit' type = "submit" class = "btn btn-primary" value='Create'>
    </div>
</form>
<a href = "${request.route_url('login')}">Already have an account?</a>
%if error:
    %for key, msg in error.items():
        <p class="alert alert-danger">
            ${msg}
        </p>
    %endfor
%endif