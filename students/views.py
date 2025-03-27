from django.shortcuts import render
from .models import Student
from django.views.generic import ListView

# Create your views here.
class StudentListView(ListView):
  model = Student
  template_name = 'student/student_list.html'
  # context_object_name的作用是自定义模板中的变量名，通常用于 ListView 等视图中，在模板里用 for 循环遍历数据
  context_object_name = 'students'
  paginate_by = 10