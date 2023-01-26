from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics
from .models import List, Task
from .serializers import ListSerializer, TaskSerializer
from rest_framework_yaml.renderers import YAMLRenderer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from django.contrib.auth.models import User

# Create your views here.

@api_view()
def test(request):
    return Response({"message": "Hi"})

class TaskItems(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request:Request):

        username = request.user.username
        user = User.objects.get(username = username)
        list = List.objects.filter(user = user)

        tasks = Task.objects.select_related('list').filter(list__in = list)
        serialized_items = TaskSerializer(tasks, many = True)

        return Response({"User" :str(user) ,"Tasks": serialized_items.data})

    def post(self, request:Request):

        list = request.data.get('list')
        user_list = List.objects.get(pk = list)

        if request.user.username == user_list.user.username:

            task = request.data.get('task')
            user_task = Task(list = user_list, task = task)
            user_task.save()

            serialized_data = TaskSerializer(user_task)

            return Response({"Message": "Succesfully added the task."}, status=status.HTTP_201_CREATED)


        else:
            return Response({"Message": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)



class ListItems(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request:Request):
        pass
    

