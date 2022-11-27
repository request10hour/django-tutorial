from django.contrib import admin

# Register your models here.
from .models import Choice, Question

# # admin을 통해 Question을 관리할 수 있도록 등록
# admin.site.register(Question)

# admin을 통해 Choice를 관리할 수 있도록 등록
# StackedInline: Choice를 Question 아래에 표시
# TabularInline: Choice를 표로 표시
class ChoiceInline(admin.TabularInline):
	# Choice 모델을 관리할 수 있도록 등록
	model = Choice
	# Choice를 추가할 수 있는 추가 폼의 개수
	extra = 3

# Question 모델을 관리할 수 있도록 등록
# ModelAdmin: Question 모델을 관리할 수 있도록 등록
class QuestionAdmin(admin.ModelAdmin):
	# fieldsets: Question 모델의 필드를 그룹으로 묶어서 표시
	fieldsets = [
		(None,					{'fields': ['question_text']}),
		('Date information',	{'fields': ['pub_date']}),
	]
	# inlines: Question 모델과 연결된 Choice 모델을 관리할 수 있도록 등록
	inlines = [ChoiceInline]
	# /admin/polls/question/ 페이지에서 확인 가능
	# list_display: Question 모델의 필드를 표로 표시
	list_display = ('question_text', 'pub_date', 'was_published_recently')
	# list_filter: Question 모델의 필드를 필터로 표시
	list_filter = ['pub_date']
	# search_fields: Question 모델의 필드를 검색할 수 있도록 표시
	search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
