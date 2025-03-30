from django import forms
from django.core.exceptions import ValidationError

from .models import Student
from grades.models import Grade


class StudentForm(forms.ModelForm):
  # “这三段代码的作用是自定义初始化：获取 Grade 表的所有数据并设置排序规则。”
  # 第一句 def __init__(self, *args, **kwargs): 只是声明了构造方法，并没有做任何实际的初始化工作。
  # 第二句 super().__init__(*args, **kwargs) 调用父类的 __init__ 方法，才会真正完成父类的初始化工作，比如初始化父类中的属性（如 fields 字段）。
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # 找到表单中的 student_grade 字段（也就是年级字段）。
    # 然后，将 student_grade的 queryset设置为：所有在 Grade 模型中的数据，并且按 grade_number 排序。
    self.fields.get('student_grade').queryset = Grade.objects.all().order_by('grade_number')

  def clean_student_name(self):
    student_name = self.cleaned_data.get('student_name')
    print(f'{student_name}')
    if len(student_name)<2 or len(student_name)>5:
      raise ValidationError('非法姓名')
    return student_name

  def clean_student_number(self):
    student_number = self.cleaned_data.get('student_number')
    student_number = str(student_number)
    if len(student_number) != 10:
      raise ValidationError('非法学号')
    return student_number

  class Meta():
    model = Student
    fields = ['student_name', 'student_gender', 'student_number', 'student_grade']