from django.urls import path
from .views import GradeList


urlpatterns = [
  path('', GradeList.as_view(),name='gradelist')
]