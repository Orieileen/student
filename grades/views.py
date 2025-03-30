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
    # 重写 ListView 的 get_queryset 方法来实现搜索功能
    # 1. 调用父类的 get_queryset 获取所有数据
    get_queryset = super().get_queryset()
    # 2. 从 GET 请求中获取搜索关键词
    search = self.request.GET.get('search')
    # 3. 如果有搜索关键词,就过滤数据
    if search:
      # 使用 Q 对象实现多字段模糊搜索
      # grade_name__icontains 表示班级名称包含关键词(不区分大小写)
      # grade_number__icontains 表示班级编号包含关键词(不区分大小写) 
      # | 表示或操作,只要满足其中一个条件就可以
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