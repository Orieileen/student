from django.db import models

# Create your models here.
class Grade(models.Model):
  grade_name = models.CharField('班级名称',max_length=50, unique=True)
  grade_number = models.CharField('班级编号',max_length=10, unique=True)

  # 输出Grade时，自动打印这个类， 返回grade_name
  def __str__(self) -> str:
    return self.grade_name
  
  class Meta:
    db_table = 'grade'
    verbose_name = '班级'
    verbose_name_plural = '班级'