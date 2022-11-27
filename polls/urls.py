from django.urls import path
from . import views

# app_name은 URLconf의 이름공간(namespace)을 구분하는데 사용됩니다.
# 이를 통해 여러개의 앱이 polls.urls를 include할 수 있습니다.
app_name = 'polls'
# urlpatterns는 URLconf의 목록입니다.
# 이 목록은 URL 패턴과 뷰를 매핑하는 것으로 이루어져 있습니다.
urlpatterns = [
	# path() 함수는 route, view, kwargs, name 인자를 받습니다.
	# route는 URL 패턴을 문자열로 받습니다.
	# view는 route에 매칭되는 URL에 호출될 view를 지정합니다.
	# kwargs는 view에 전달되는 추가 인자를 딕셔너리로 받습니다.
	# name은 URL에 이름을 붙여 참조하기 쉽게 합니다.

	# 제네릭 뷰를 사용할 때는 항상 name 인자를 지정해야 합니다.
	path('', views.IndexView.as_view(), name='index'),
	path('<int:pk>/', views.DetailView.as_view(), name='detail'),
	path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
	# int:question_id는 question_id에 해당하는 값을 뷰에 전달합니다.
	# 이 패턴은 /polls/5/와 같은 URL에 매칭됩니다.
	path('<int:question_id>/vote/', views.vote, name='vote'),
]
# app_name과 urlpatterns는 polls.urls 모듈의 전역 변수입니다.
# 이 변수들은 polls.urls 모듈을 include할 때 사용됩니다.
# html 파일에서 {% url %} 템플릿 태그를 사용할 때도 이 변수들을 사용합니다.
# {% url 'polls:detail' question.id %}와 같이 사용합니다.
# 이는 polls:detail이라는 URL 패턴을 찾아 question.id를 전달합니다.
