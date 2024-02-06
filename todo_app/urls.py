from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('add_task',views.add_task,name='add_task'),
    path('task/<str:pk>',views.task,name='task'),
    path('change/<str:pk>',views.change,name='change'),
    path('delete',views.delete,name='delete'),
    path('edit/<str:pk>',views.edit,name='edit')
]