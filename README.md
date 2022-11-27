수정하였고, 주석이 추가되어있는 내용은 다음과 같습니다.

mysite.urls
mysite.settings
changes
	'polls.apps.PollsConfig'
	timezone = 'asia/seoul'

how to add polls app to project
command : py manage.py startapp polls
	- polls/
		- __init__.py
		- admin.py
		- apps.py
		- migrations/
			- __init__.py
		- models.py
		- tests.py
		- views.py

polls.migrations << py manage.py makemigrations polls
before migration edit polls/models.py

polls.models
polls.admin
polls.urls
polls.views
polls.tests

templates
	- polls/
		- index.html
		- detail.html
		- results.html

static
	- polls/
		- style.css
