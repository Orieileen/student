from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Grade
# Create your views here.
class GradeListView(ListView):
  model = Grade
  template_name = 'grade/grade_list.html'
  fields = ['grade_name', 'grade_number']
  # 为model=Grade起上下文名字。相当于 render('grades':grades) 
  context_object_name = 'grades'

  def get_queryset(self):
    queryset = super().get_queryset()
    search = self.request.GET.get('search')
    if search:
      queryset = 