from django.urls import path
from .views import Grade_ListView, Grade_CreateView, Grade_UpdateView


urlpatterns = [
  path('', Grade_ListView.as_view(),name='gradelist'),
  path('create/', Grade_CreateView.as_view(), name='gradecreate'),
  path('<int:pk>/update/', Grade_UpdateView.as_view(), name='gradeupdate'),
]