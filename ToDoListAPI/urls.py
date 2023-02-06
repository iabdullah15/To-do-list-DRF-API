from django.urls import path
from . import views

urlpatterns = [
    path('', views.test),
    path('tasks', views.TaskItems.as_view()),
    path('lists', views.ListItems.as_view()),
    path('list/<int:id>', views.SingleListItem.as_view()),
    path('task/<int:id>', views.SingleTaskItem.as_view()),
]