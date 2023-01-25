from django.urls import path
from . import views

urlpatterns = [
    path('', views.test),
    path('test', views.Test.as_view()),
]