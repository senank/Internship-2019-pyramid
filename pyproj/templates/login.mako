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
    <div class = 'form-row'>
        <div class = 'col' >
            <label>Username:<input type="text" class = 'form-control' name = "username" placeholder="username"></label>
        </div>
        <div class = 'col' >
            <label>Password:<input type = "password" class = 'form-control' name = "password" placeholder = "password"></label>
        </div>
    </div> 
    <div class = 'form-group' >  
        <input name = 'login_submit' type = "submit" class = "btn btn-primary" value='Sign In'>
    </div>   
</form>
</div>
<div>
    <a href="${request.route_url('create')}">Create an Account</a>
</div>