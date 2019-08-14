<%inherit file="layout.mako"/>
<div class="content">
  <%
  url = request.path.split('/')
  path = url[-1].upper()
  %>


  <h1><span class="font-semi-bold">Forbidden Access</span></h1>
  %if request.authenticated_userid is not None:
    <p class='lead'>Access Denied</p>
  %else:
    <p class='lead'>Login to view: ${path} PAGE</p>
  %endif
</div>
