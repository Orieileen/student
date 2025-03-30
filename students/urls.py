from django.urls import path
# Django app 内部：用 from .views import *
# Django app 之间：用 from app_name.views import *
from .views import *

urlpatterns = [
  path('', StudentListView.as_view(), name='studentlist'),
  path('studentcreate/', StudentCreateView.as_view(), name='studentcreate'),
]