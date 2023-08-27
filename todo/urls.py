from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('' , viewset=views.TodoViewset)

urlpatterns = [
    # path('' , views.TodoView),
    # path('<int:pk>' , views.update_View),
    path('cbv/' , views.ListTodoView.as_view()),
    path('cbv/<int:pk>' , views.UpdateTodoView.as_view()),
    # path('mix/' , views.TodoMixinListView.as_view()),
    # path('mix/<int:pk>' , views.TodoUpdateMixinView.as_view()),
    # path('generic/' , views.TodoListGenericView.as_view()),
    # path('generic/<int:pk>' , views.TodoUpdateGenericView.as_view()),
    # path('viewset/' , include(router.urls)),
    # path('generic/nest/' , views.TodoNestedView.as_view()),

]