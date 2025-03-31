from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Student
from .form import StudentForm

# Create your views here.
class StudentListView(ListView):
  model = Student
  template_name = 'student/student_list.html'
  # context_object_name的作用是自定义模板中的变量名，通常用于 ListView 等视图中，在模板里用 for 循环遍历数据
  context_object_name = 'studentlist'
  paginate_by = 1

class StudentCreateView(CreateView):
  model = Student
  template_name = 'student/student_form.html'
  form_class = StudentForm
  success_url = reverse_lazy('studentlist')

  # 重写def form_valid():
  def form_valid(self, form):
    # 接受字段
    student_name = form.cleaned_data.get('student_name')
    student_number = form.cleaned_data.get('student_number')
    # 拼接字段作为登录账号和密码
    username = student_name + '_' + student_number
    password = student_number[-6:]
    users = User.objects.filter(username=username)#filter()需要指定查询条件，格式为 字段名=值  SELECT * FROM auth_user WHERE username='zhangsan';
    if users.exists():
      user = user.first()# 取第一条数据
    else:
      # 创建auth_user表记录
      # objects是表管理器，下面就是管理User表创建user
#        create_user：会自动加密密码（存入数据库时，密码不是明文）。
#       不会创建超级用户（is_superuser=False）。
#       默认 is_active=True（账户可用）。
#       默认 is_staff=False（不是管理员）。
      user = User.objects.create_user(username=username, password=password)
    # 写入student
    # form.instance 代表的是 表单提交时的模型实例
    # 将刚刚创建的user 这一行赋值给Student表的一对一字段user，Student数据表中就会有例：userid=2，auth_user就有一行id为2的user  就是把两行数据关联了
    form.instance.user = user
    form.save()

  # return 语句的主要目的是告诉视图如何处理请求后的行为。
  # 具体来说，return 是为了确保视图在表单提交并成功验证后能返回一个合适的响应（比如重定向或呈现页面）。
    return JsonResponse({
      'status': 'success'
    },status=200)


class StudentUpdateView(UpdateView):
  model = Student
  template_name = 'student/student_form.html'
  form_class = StudentForm
  success_url = reverse_lazy('studentlist')

  def form_valid(self, form):
    student = form.save(commit=False)#form.save(commit=False) 先不保存表单，而是创建一个 student 实例，让你可以手动修改它的属性。form.save()默认行为commit=True
    if 'student_name' in form.changed_data or 'student_number' in form.changed_data:
      student.user.username = form.cleaned_data.get('student_name') + form.cleaned_data.get('student_number')
      student.user.password = make_password(form.cleaned_data.get('student_number')[-6:])
      student.user.save()#先保存student关联的user，确保username和password的更改生效。

    student.save()#最后保存 student，确保整个数据对象更新到数据库。

# ✅ commit=False 允许你先修改数据，再决定什么时候提交到数据库。
# ✅ 适用于需要额外处理字段，或者有外键关联的情况。例：在更改姓名和学号时，同时更改auth_user用户名和密码
# ✅ 可以减少不必要的数据库写入，提高性能。

# 为什么在 CreateView 中可以直接操作 username 而不需要先保存 form：
# 在 CreateView 中，form.instance 代表的是一个未保存的 Student 实例。
# 你可以直接对 form.instance 进行操作（如将 user 关联到 Student），并在最终调用 form.save() 时，Django 会在同一个 save 调用中，将 Student 和 User 同时保存。
# 由于 CreateView 的 form.instance 只是一个未保存的对象，你可以在保存之前修改它的属性，并且不需要额外的 commit=False 语句。
# 通过 form.instance.user = user，你直接为 Student 赋值一个关联的 user，然后调用 form.save() 保存整个对象（Student 和 User）。

# 为什么在 UpdateView 中需要 commit=False：
# 在 UpdateView 中，form.save() 默认是将表单的数据直接保存到数据库，这意味着如果你没有使用 commit=False，student 和它关联的 user 会被同时保存，这可能导致数据还未修改完之前就已保存。
# commit=False 的作用是：它让你先获得一个未保存的 student 实例，这样你可以在保存之前修改 student 和 user 的属性。
# 在 UpdateView 中，student 已经存在于数据库中，你需要先修改 user（比如更新 username 和 password），再调用 student.save() 保存 student 对象。如果你不先修改 user，那么 user 对象的变化就不会保存到数据库。
# 这样做的目的是避免在 student.save() 之前，user 的数据就已经被保存，造成数据不一致。

    return HttpResponseRedirect(self.success_url)
# success_url：
# success_url 是 UpdateView 默认的行为，当 form_valid() 成功时，Django 会自动使用这个 URL 重定向到指定的页面。如果你设置了 success_url，Django 会在 form_valid() 后自动执行重定向操作。
# redirect('studentlist')：
# 在 form_valid() 方法中，你也使用了 redirect('studentlist') 来手动进行重定向。这个重定向会覆盖默认的 success_url，因为你明确指定了重定向的目标。success_url就可以删除了

# 以上代码没有完整的后端验证, cleaned_date实际上并不是后端验证的一部分，而是数据提取的步骤。你从已经通过验证的表单数据中提取出具体字段的值。 cleaned_data 是经过 Django 自动验证后，保证数据格式和规则正确的字段数据。