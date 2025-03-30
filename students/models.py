from django.db import models

from django.contrib.auth.models import User
from grades.models import Grade

# Create your models here.
STUDENT_GENDER_CHOICES= [
  ('M', '男'),
  ('F', '女'),
]

class Student(models.Model):
  student_name = models.CharField('学生姓名', max_length=100)
  student_gender = models.CharField('性别', choices=STUDENT_GENDER_CHOICES, max_length=1)
  student_number = models.IntegerField('学号', unique=True)

  # 用 OneToOneField 主要是当你想给 User 模型扩展额外信息时，比如创建 Profile 个人信息表，每个 User 只能对应一个 Profile,
  # User 是 Django 内置的用户模型，对应auth_user表它存储了用户的基本信息，比如用户名、密码、邮箱等。
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  # related_name='students':反向查询名,允许从 Grade 反向查询所有属于该年级的 Student。
  student_grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='students')

  # 这个方法是 Python 魔法方法（dunder method）,用于返回模型实例的字符串表示，主要作用是：
  # 1.Admin 显示更友好 2.打印实例时更直观 3.查询时调试更方便
  def __str__(self) -> str:
    return self.user.username
  
  class Meta:
    db_table = 'student'
    verbose_name = '学生信息表'
    verbose_name_plural = '学生信息表'