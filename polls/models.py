import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
# Create your models here.

# Question 모델을 정의
# Question 모델은 질문과 발행일을 저장하는 필드를 가짐
# Question 모델은 __str__() 메서드를 가짐
# Question 모델은 was_published_recently() 메서드를 가짐
class Question(models.Model):
	# Question 모델의 속성들을 정의
	# 질문 내용을 저장할 속성
	# CharField는 글자 수가 제한된 텍스트를 정의할 때 사용
	question_text = models.CharField(max_length=200)
	# 질문이 게시된 날짜를 저장할 속성
	# DateTimeField는 날짜와 시간을 저장할 수 있는 속성입니다.
	# verbose_name은 속성의 이름을 지정합니다.
	# 이 속성은 관리자 페이지에서 사용됩니다.
	pub_date = models.DateTimeField('date published')
	# __str__() 메서드는 객체를 문자열로 표현할 때 사용됩니다.
	# 이 메서드는 객체를 표현하는데 사용됩니다.
	# 이 메서드를 정의하지 않으면, 객체를 표현하는데 Question object(또는 다른 모델 이름)라는 문자열이 사용됩니다.
	# 이 메서드를 정의하면, 객체를 표현하는데 question_text 속성의 값이 사용됩니다.
	def __str__(self):
		return self.question_text
	# display() decorator를 해당 메서드( :file:`polls/models.py`에 있는)에 사용하면 다음과 같이 개선할 수 있습니다.
	# 앞의 @는 데코레이터라고 부릅니다.
	# 데코레이터는 함수를 수정하지 않고도 함수의 동작을 변경할 수 있게 해줍니다.
	@admin.display(
		# Boolean 속성을 사용하면, True일 때만 해당 메서드가 표시됩니다.
		boolean=True,
		# ordering 속성을 사용하면, 해당 메서드의 값으로 정렬할 수 있습니다.
		ordering='pub_date',
		# description 속성을 사용하면, 해당 메서드의 이름을 지정할 수 있습니다.
		description='Published recently?',
	)
	# was_published_recently() 메서드는 Question 객체가 최근에 게시되었는지를 판단합니다.
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

# Choice 모델을 정의
# Choice 모델은 질문과 선택지 내용을 저장하는 필드를 가짐
# Choice 모델은 __str__() 메서드를 가짐
# Choice 모델은 votes 속성을 가짐
class Choice(models.Model):
	# Choice 모델의 속성들을 정의
	# 질문을 저장할 속성
	# ForeignKey는 다른 모델에 대한 링크를 의미합니다.
	# 이 속성은 Question 모델에 대한 링크를 의미합니다.
	# on_delete=models.CASCADE는 Question 객체가 삭제되면, 연결된 Choice 객체도 삭제된다는 의미입니다.
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	# 선택지 내용을 저장할 속성
	# CharField는 글자 수가 제한된 텍스트를 정의할 때 사용
	choice_text = models.CharField(max_length=200)
	# 투표 수를 저장할 속성
	# IntegerField는 정수를 저장할 때 사용
	votes = models.IntegerField(default=0)
	# __str__() 메서드는 객체를 문자열로 표현할 때 사용됩니다.
	# 이 메서드는 객체를 표현하는데 사용됩니다.
	# 이 메서드를 정의하지 않으면, 객체를 표현하는데 Choice object(또는 다른 모델 이름)라는 문자열이 사용됩니다.
	# 이 메서드를 정의하면, 객체를 표현하는데 choice_text 속성의 값이 사용됩니다.
	def __str__(self):
		return self.choice_text
