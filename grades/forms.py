from django import forms

from .models import Grade


# 所有字段验证都在ModelForm里，调用后就不用自己写
class GradeForm(forms.ModelForm):

  class Meta:
    model = Grade
    fields = ['grade_name', 'grade_number']
