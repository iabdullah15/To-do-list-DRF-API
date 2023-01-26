from django.urls import path
from . import views

urlpatterns = [
    path('', views.test),
    path('tasks', views.TaskItems.as_view()),
    # path('list', views.ListItems.as_view()),
]