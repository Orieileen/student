from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Grade
from .forms import GradeForm
from django.urls import reverse_lazy

# Create your views here.
class Grade_ListView(ListView):
  model = Grade
  fields = ['grade_name','grade_number']
  template_name = 'grade/grade_list.html'
  paginate_by = 1
  # context_object_name的作用是自定义模板中的变量名，通常用于 ListView 等视图中，在模板里用 for 循环遍历数据
  context_object_name = 'gradelist'

  def get_queryset(self) -> QuerySet[Any]:
    get_queryset = super().get_queryset()
    search = self.request.GET.get('search')
    if search:
      get_queryset = get_queryset.filter(
        Q(grade_name__icontains=search) | Q(grade_number__icontains=search)
      )
    return get_queryset
  
class Grade_CreateView(CreateView):
  model = Grade
  template_name = 'grade/grade_form.html'
  form_class = GradeForm
  success_url = reverse_lazy('gradelist')

class Grade_UpdateView(UpdateView):
  model = Grade
  template_name = 'grade/grade_form.html'
  form_class = GradeForm
  success_url = reverse_lazy('gradelist')

class Grade_DeleteView(DeleteView):
  model = Grade
  template_name = 'grade/grade_delete_confirm.html'
  success_url = reverse_lazy('gradelist')