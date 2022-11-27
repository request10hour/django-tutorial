from django.contrib import admin

# Register your models here.
from .models import Question

# admin을 통해 Question을 관리할 수 있도록 등록
admin.site.register(Question)
