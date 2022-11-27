from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# 제네릭 뷰를 사용하면 뷰를 작성하는 코드를 줄일 수 있습니다.
# 제네릭 뷰는 장고에서 제공하는 뷰의 기본 구조를 재사용하는 뷰입니다.
# generic.ListView 는 Question 객체의 목록을 보여주는 뷰를 만들어 줍니다.
# 개체 목록 표시
class IndexView(generic.ListView):
	# template_name 속성은 기본 템플릿 이름을 지정합니다.
	template_name = 'polls/index.html'
	# ListView는 자동으로 context 변수를 생성합니다.
	# context 변수는 템플릿에 전달되는 객체의 이름을 지정합니다.
	# 기본값은 question_list입니다.
	# context_object_name 속성을 사용하여 변경할 수 있습니다.
	# context_object_name = 'latest_question_list'
	context_object_name = 'latest_question_list'
	# get_queryset() 메서드는 context 변수에 전달할 객체를 반환합니다.
	# get_queryset() 메서드는 Question.objects.all()을 반환합니다.
	# Question.objects.all()은 Question 모델의 모든 객체를 반환합니다.
	# Question.objects.order_by('-pub_date')[:5]는 Question 모델의 객체를 발행 날짜의 역순으로 정렬하고, 그 중에서 5개만 반환합니다.
	def get_queryset(self):
		"""최근에 발행된 5개의 Question을 반환합니다."""
		# pub_date__lte=timezone.now()는 pub_date <= timezone.now()와 같습니다.
		# __lte는 less than or equal to의 약자입니다.
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# generic.DetailView는 특정 타입의 객체에 대한 상세 정보를 보여주는 뷰입니다.
# 특정 개체 유형에 대한 세부 정보 페이지 표시
# DetailView는 특정 Question에 대한 상세 정보를 보여주는 뷰입니다.
class DetailView(generic.DetailView):
	# Question 모델을 사용합니다.
	model = Question
	# template_name 속성은 기본 템플릿 이름을 지정합니다.
	template_name = 'polls/detail.html'
	# get_queryset() 메서드는 context 변수에 전달할 객체를 반환합니다.
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

# ResultsView는 특정 Question에 대한 투표 결과를 보여주는 뷰입니다.
class ResultsView(generic.DetailView):
	# Question 모델을 사용합니다.
	model = Question
	# template_name 속성은 기본 템플릿 이름을 지정합니다.
	template_name = 'polls/results.html'

# vote 메서드는 POST 요청만 처리하므로, GET 요청에 대해서는 404 에러를 발생시킵니다.
# 이는 장고의 보안 기능으로, 사용자가 URL을 직접 입력해서 투표를 두 번 할 수 없도록 합니다.
# html 폼에서 POST 방식으로 요청을 보내기 때문에, 이 함수는 POST 방식으로 요청이 들어온 경우에만 동작합니다.
def vote(request, question_id):
	# get_object_or_404()는 Question 모델에서 pk(primary key)가 question_id인 레코드를 가져옵니다.
	# 만약 해당 레코드가 없으면 Http404 에러를 발생시킵니다.
	question = get_object_or_404(Question, pk=question_id)
	# try로 시작해서 except로 끝나는 코드 블록은
	# 선택된 Choice가 POST 데이터에 존재하지 않는 경우에
	# 발생하는 KeyError를 잡아냅니다.
	try:
		# selected_choice는 Choice 모델의 객체
		# choice set은 Choice 모델의 객체들의 집합
		# request.POST['choice']는 선택된 Choice의 pk
		# request.POST는 사용자가 POST 방식으로 보낸 데이터를 담고 있는 객체
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	# KeyError가 발생하면 except로 넘어가고
	# except로 넘어가면 다시 detail.html로 돌아감
	# DoesNotExist는 get() 메서드가 해당 레코드가 없을 때 발생하는 예외
	except (KeyError, Choice.DoesNotExist):
		# render() 함수는 템플릿을 렌더링하고
		# HttpResponse 객체를 반환합니다.
		# render() 함수는 세 개의 인자를 받습니다.
		# request: 사용자의 요청
		# 'polls/detail.html': 템플릿의 위치
		# {'question': question, 'error_message': "You didn't select a choice.",}: 템플릿에 전달할 데이터
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	# except로 넘어가지 않으면
	# selected_choice.votes를 1 증가시키고
	# selected_choice.save()를 호출하여
	# 데이터베이스에 변경사항을 저장
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# HttpResponseRedirect는 사용자가
		# POST 방식으로 데이터를 보낸 후에
		# 데이터를 보낸 주소로 다시 보내는 클래스
		# reverse()는 URL 패턴의 이름을 받아서
		# URL 패턴에 해당하는 URL을 반환하는 함수
		# reverse()의 첫 번째 인자는 URL 패턴의 이름
		# 두 번째 인자는 URL 패턴에 해당하는 뷰 함수에 전달할 인자
		# reverse()는 URL 패턴에 해당하는 뷰 함수에 전달할 인자를
		# 딕셔너리 형태로 받음
		return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
