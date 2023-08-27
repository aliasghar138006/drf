from django.shortcuts import render
from django.http import Http404
from .serializers import TodoSerializer , TodoUserSerializer
from .models import Todo
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics , mixins , viewsets
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination , LimitOffsetPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


User = get_user_model()

# Create your views here.

# region defapi_view
@api_view(['GET' , 'POST'])
def TodoView(request:Request):
    if (request.method == 'GET'):
        todos = Todo.objects.order_by('peririty').all()
        todo_serialized = TodoSerializer(todos , many=True)
        return Response(todo_serialized.data , status.HTTP_200_OK)
    elif (request.method == 'POST'):
        serializer = TodoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status.HTTP_201_CREATED)
        return Response(None , status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT' , 'DELETE'])
def update_View(request:Request , pk):
    try:
        todo = Todo.objects.filter(pk=pk).first()
    except Todo.DoesNotExist():
        return Http404

    # todo = Todo.objects.filter(pk=pk).first()
    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data , status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = TodoSerializer(todo , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status.HTTP_202_ACCEPTED)
        return Response(None , status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        todo.delete()
        return Response(None , status.HTTP_202_ACCEPTED)
#endregion


#region cbv
class ListTodoView(APIView):
    @extend_schema(
        request=TodoSerializer,
        responses={201: TodoSerializer},
        description='this is class Based View'
    )
    def get(self , request:Request):
        todos = Todo.objects.order_by('peririty').all()
        todo_serialized = TodoSerializer(todos , many=True)
        return Response(todo_serialized.data , status.HTTP_200_OK)

    def post(self,request:Request):
        serializer = TodoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status.HTTP_201_CREATED)
        return Response(None , status.HTTP_400_BAD_REQUEST)




class UpdateTodoView(APIView):
    def get_object(self , pk:int):
        try:
            todo = Todo.objects.get(pk=pk)
            return todo
        except Todo.DoesNotExist():
            return Response(None , status.HTTP_404_NOT_FOUND)

    def get(self , request:Request , pk:int):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data , status.HTTP_200_OK)

    def put(self , request:Request , pk:int):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status.HTTP_202_ACCEPTED)
        else:
            return Response(None , status.HTTP_400_BAD_REQUEST)

    def delete(self , request:Request , pk:int):
        todo = self.get_object(pk)
        todo.delete()
        return Response(None , status.HTTP_202_ACCEPTED)

#endregion

#region mixins

class TodoMixinListView(mixins.ListModelMixin,mixins.CreateModelMixin , generics.GenericAPIView ):
    queryset = Todo.objects.order_by('peririty').all()
    serializer_class = TodoSerializer
    pagination_class = LimitOffsetPagination

    def get(self , request):
        return self.list(request)
    
    def post(self , request):
        return self.create(request)
    



class TodoUpdateMixinView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Todo.objects.order_by('peririty').all()
    serializer_class = TodoSerializer

    def get(self , request ,pk:int):
        return self.retrieve(request ,pk)
    
    def put(self , request ,pk:int):
        return self.update(request , pk)
    
    def delete(self , request , pk:int):
        return self.destroy(request ,pk)
#endregion

#region pagination
class TodoPaginationView(PageNumberPagination):
    page_size = 1
#endregion

#region generic

class TodoListGenericView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('peririty').all()
    serializer_class = TodoSerializer
    pagination_class = TodoPaginationView
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self , request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    


class TodoUpdateGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by('peririty').all()
    serializer_class = TodoSerializer

    def get(self , request , pk:int):
        return self.retrieve(request , pk)
    
    def put(self, request, pk:int):
        return self.update(request , pk)
    
    def delete(self , request , pk:int):
        return self.destroy(request , pk)
#endregion





#region viewset
class TodoViewset(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by('peririty').all()
    serializer_class = TodoSerializer
#endregion



#region nested-serializer
class TodoNestedView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = TodoUserSerializer

    def get(self, request):
        return self.list(request)
#endregion

