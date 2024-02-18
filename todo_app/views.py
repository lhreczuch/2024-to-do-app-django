from django.shortcuts import render,redirect
from .models import Task,Comment
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RegisterForm, TaskForm, CommentForm
from django.contrib.auth import login

from rest_framework.views import APIView

from .serializers import TaskSerializer, UserSerializer
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth.models import User

import jwt,datetime
# Create your views here.
@login_required(login_url='/login')
def index(request):
    tasks = Task.objects.all()
    if request.method =="POST":
        task_id = request.POST['task_id']
        if Task.objects.filter(id=task_id, is_done=True):
            Task.objects.filter(id=task_id).update(is_done=False)
        else:
            Task.objects.filter(id=task_id).update(is_done=True)
        
    
    return render(request, 'main/index.html',{'tasks':tasks})

def register(request):
    if request.method =="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request,'registration/register.html',{'form':form})

@login_required(login_url='/login')
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
    return render(request,'main/add_task.html',{'form':form})

@login_required(login_url='/login')
def task(request,pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task = Task.objects.filter(id = pk).first()
            comment.save()
            return redirect(f'/task/{pk}')
    else:
        form = CommentForm()
        task = Task.objects.filter(id=pk).first()
        comments = Comment.objects.filter(task=task.id)
    return render(request,'main/task.html',{'form':form,'task':task,'comments':comments})

@login_required(login_url='/login')
def change(request,pk):
    if request.method =="POST":
        task_id = request.POST['task_id']
        if Task.objects.filter(id=task_id, is_done=True):
            Task.objects.filter(id=task_id).update(is_done=False)
        else:
            Task.objects.filter(id=task_id).update(is_done=True)
        return redirect(f'/task/{pk}')
    
@login_required(login_url='/login')
def delete(request):
    if request.method == "POST":
        task_id = request.POST['task_id']
        Task.objects.filter(id=task_id).first().delete()
        return redirect('/')

@login_required(login_url='/login')
def edit(request,pk):
    task = Task.objects.get(id=pk)
    if request.method == "POST":
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = TaskForm(instance=task)
    return render(request, 'main/edit.html',{'form':form})
    


"""
api views below
"""

@api_view(['GET'])
def apiOverView(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed("unathenticated")
    
    try:
        payload = jwt.decode(token, 'secret',algorithms=['HS256'])
        
    except:
        raise AuthenticationFailed('unathenticated or token expired!')
    return JsonResponse("API BASE POINT. Now you are authenticated", safe=False)


@api_view(['GET'])
def task_list(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed("unathenticated")
    
    try:
        payload = jwt.decode(token, 'secret',algorithms=['HS256'])
        
    except:
        raise AuthenticationFailed('unathenticated or token expired!')
    
    task = Task.objects.all()
    serializer = TaskSerializer(task,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def task_details(request,pk):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed("unathenticated")
    
    try:
        payload = jwt.decode(token, 'secret',algorithms=['HS256'])

    except:
        raise AuthenticationFailed('unathenticated or token expired!')
    
    task = Task.objects.filter(id=pk).first()
    serializer = TaskSerializer(task,many=False)
    return Response(serializer.data)


# to do: server has to recognize which user sends request to create task and has to assign him to 'author field'

@api_view(['POST'])
def create_task(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed("unathenticated")
    
    try:
        payload = jwt.decode(token, 'secret',algorithms=['HS256'])
        
    except:
        raise AuthenticationFailed('unathenticated or token expired!')
    serializer = TaskSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def update_task(request,pk):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed("unathenticated")
    
    try:
        payload = jwt.decode(token, 'secret',algorithms=['HS256'])
        
    except:
        raise AuthenticationFailed('unathenticated or token expired!')
    task = Task.objects.filter(id=pk).first()
    serializer = TaskSerializer(instance=task,data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_task(request,pk):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed("unathenticated")
    
    try:
        payload = jwt.decode(token, 'secret',algorithms=['HS256'])
        
    except:
        raise AuthenticationFailed('unathenticated or token expired!')
    task = Task.objects.get(id=pk)
    
    task.delete()
    return Response("deleted item !")


@api_view(['POST'])
def api_register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def api_login(request):
    username = request.data['username']
    password = request.data['password']

    user = User.objects.filter(username=username).first()

    if user is None:
        raise AuthenticationFailed('User not found')
    
    if not user.check_password(password):
        raise AuthenticationFailed('incorrect password')
    
    payload = {
        'id' : user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload,'secret', algorithm='HS256') 
    
    response = Response()

    response.set_cookie(key='jwt',value=token)
    response.data = {
        'jwt':token
    }
    return response
    

@api_view(['POST'])
def api_logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success. logged out'
    }
    return response
