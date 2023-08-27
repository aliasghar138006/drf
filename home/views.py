from django.shortcuts import render
from todo.models import Todo
from django.http import HttpRequest , HttpResponse ,JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status



# Create your views here.


def home_page(request):
    context = {
        'todos' : Todo.objects.all()
    }
    return render(request , 'home/index.html' , context)


# def home_api(request: HttpRequest):
#     data = {
#         'name' : "aliasghar"
#     }
#     return JsonResponse(data)

@api_view(['GET'])
def home_api(request: Request):
    todo = list(Todo.objects.order_by('peririty').all().values('title', 'is_done' , 'id'))
    return Response({'todo':todo} , status.HTTP_200_OK)

