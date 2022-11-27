from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from django.urls import reverse

from .models import Question

# TestCase는 테스트를 위한 특별한 유형의 클래스
# 테스트를 위한 특별한 기능을 제공
class QuestionModelTests(TestCase):
	# 테스트 메소드는 test로 시작
	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		# assertIs() 메소드는 첫번째 인자가 두번째 인자와 같은지 확인
		# 같지 않으면 테스트 실패
		# 같으면 테스트 성공
		# 이 테스트는 was_published_recently() 메소드가 False를 반환하는지 확인
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
	def test_no_questions(self):
		response = self.client.get(reverse('polls:index'))
		# assertEqual() 메소드는 첫번째 인자와 두번째 인자가 같은지 확인
		# assertEqual() 메소드는 타입을 확인하지 않음
		# 타입을 확인하려면 assertEqual() 메소드 대신 assertIs() 메소드를 사용
		self.assertEqual(response.status_code, 200)
		# assertContains() 메소드는 response 객체가 특정 문자열을 포함하는지 확인
		self.assertContains(response, "No polls are available.")
		# assertQuerysetEqual() 메소드는 response 객체의 context 변수가 특정 쿼리셋과 같은지 확인
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_past_question(self):
		question = create_question(question_text="Past Question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], [question])

	def test_future_question(self):
		create_question(question_text="Future question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_future_question_and_past_question(self):
		question = create_question(question_text="Past question", days=-30)
		create_question(question_text="Future question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], [question])

	def test_two_past_questions(self):
		question1 = create_question(question_text="Past Question 1", days=-30)
		question2 = create_question(question_text="Past Question 2", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1])

class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		future_question = create_question(question_text="Future Question", days=5)
		url = reverse('polls:detail', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		past_question = create_question(question_text="Past Question", days=-5)
		url = reverse('polls:detail', args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)
