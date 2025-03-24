from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from .models import Grade

# Create your views here.
class GradeList(ListView):
  model = Grade
  fields = ['grade_name','grade_number']
  template_name = 'grade/grade_list.html'
  paginate_by = 1
  context_object_name = 'gradelist'

  def get_queryset(self) -> QuerySet[Any]:
    get_queryset = super().get_queryset()
    search = self.request.GET.get('search')
    if search:
      get_queryset = get_queryset.filter(
        Q(grade_name__icontains=search) | Q(grade_number__icontains=search)
      )
    return get_queryset