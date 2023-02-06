from django.shortcuts import render, get_object_or_404
import datetime as dt
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
from django.http import QueryDict

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

            print(request.user.username, user_list.title)

            serialized_data = TaskSerializer(user_task)

            return Response({"Message": "Succesfully added the task."}, status=status.HTTP_201_CREATED)


        else:
            return Response({"Message": "You are not authorized."}, status=status.HTTP_403_FORBIDDEN)



class ListItems(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request:Request):
    
        lists = List.objects.filter(user = request.user)

        serialized_data = ListSerializer(lists, many = True)
        return Response({"Lists": serialized_data.data})

    
    def post(self, request:Request):
        
        list_title = request.data.get('title')
        
        if list_title:

            list = List.objects.create(user = request.user, title = list_title)
            list.save()

            return Response({"message": "List succesfully created."}, status=status.HTTP_201_CREATED)

        return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)


class SingleListItem(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request:Request, id):
        
        list_title = request.data.get('title')

        if list_title:
            
            list = get_object_or_404(List, pk = id)

            if list.user == request.user:

                list.title = list_title
                list.last_updated = dt.datetime.now()
                list.save()

                return Response({"message": "updated sucessfully"}, status=status.HTTP_204_NO_CONTENT)

            else:
                return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
            

        return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request:Request, id):

        list = get_object_or_404(List, pk = id)

        if list.user == request.user or request.user.is_staff:

            list.delete()
            return Response({"message": "deleted succesfully"})

        return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)


class SingleTaskItem(APIView):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request:Request, id):

        task = get_object_or_404(Task, pk = id)

        if task.list.user == request.user or request.user.is_staff:

            serialized_data = TaskSerializer(task)

            return Response(serialized_data.data, status=status.HTTP_200_OK)

        return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)


    def patch(self, request:Request, id):

        try:
            my_model = Task.objects.get(pk=id)
        except Task.DoesNotExist:
            return Response({"error": "MyModel instance not found."}, status=status.HTTP_404_NOT_FOUND)

        task = request.data.get('task')
        
        if not task:
            task = my_model.task
            my_status = request.data.get('status')

            print("not task")

            if not my_status:
                my_status = my_model.status

            myDict = {
                'task':task,
                'status': my_status
            }

            query_dict = QueryDict('', mutable=True)
            query_dict.update(myDict)

            serializer = TaskSerializer(my_model, data=query_dict, partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response (serializer.data, status=status.HTTP_204_NO_CONTENT)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        else:

            print("task")

            serializer = TaskSerializer(my_model, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                return Response (serializer.data, status=status.HTTP_204_NO_CONTENT)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request:Request, id):

        task = get_object_or_404(Task, pk = id)

        if task.list.user == request.user or request.user.is_staff:

            task.delete()
            return Response({"message": "deleted"}, status=status.HTTP_200_OK)

        return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)