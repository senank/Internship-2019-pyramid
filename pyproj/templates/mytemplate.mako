<%inherit file="layout.mako"/>
<div class="content">
  <h1><span class="font-semi-bold">Pyramid</span> <span class="smaller">Starter project</span></h1>
  <p class="lead">Welcome to <span class="font-normal">${project}</span>, a&nbsp;Pyramid application generated&nbsp;by<br><span class="font-normal">Cookiecutter</span>.</p>
  <a href="${request.route_path('todo_list')}">ToDo Page<a>

</div>
