from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

# Create your views here.

@api_view()
def test(request):
    return Response({"message": "Hi"})

class Test(APIView):

    def get(self, request:Request):
        return Response({"message": "Hi"})
