from django.shortcuts import render,redirect
from .models import Task,Comment
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RegisterForm, TaskForm, CommentForm
from django.contrib.auth import login

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

def change(request,pk):
    if request.method =="POST":
        task_id = request.POST['task_id']
        if Task.objects.filter(id=task_id, is_done=True):
            Task.objects.filter(id=task_id).update(is_done=False)
        else:
            Task.objects.filter(id=task_id).update(is_done=True)
        return redirect(f'/task/{pk}')
