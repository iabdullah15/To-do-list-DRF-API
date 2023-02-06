from rest_framework import serializers
from .models import List, Task
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):

    list_title = serializers.SerializerMethodField(method_name='get_list_title')

    def get_list_title(self, obj:Task):
        return obj.list.title

    class Meta:
        model = Task
        fields = ['id', 'list_title', 'task', 'status']
        extra_kwargs = {
            'task': {'allow_null': True, 'default': 'N/A'},
        }