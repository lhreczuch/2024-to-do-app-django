from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.apiOverView,name='api-overview'),
    path('login',views.api_login,name="api_login"),
    path('register',views.api_register,name="api_register"),
    path('task_list',views.task_list,name='task_list'),
    path('task_details/<str:pk>',views.task_details,name='task_details'),
    path('create_task',views.create_task,name='create_task'),
    path('update_task/<str:pk>',views.update_task,name='update_task'),
    path('delete_task/<str:pk>',views.delete_task,name='delete_task'),
    path('logout',views.api_logout,name="api_logout"),
]