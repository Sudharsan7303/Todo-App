from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    
    context = {
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', context)

def register(request):
    # if request.user.is_authenticated:
    #     return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')


        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return redirect('register')
        
        if password != password2:
            messages.error(request, 'Re-entered password did not match')
            return redirect('register')

        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Error, username already exists, User another.')
            return redirect('register')
        
        get_all_users_by_email = User.objects.filter(email=email)
        if get_all_users_by_email:
            messages.error(request, 'Error, email already exists, User another.')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    return render(request, 'todoapp/register.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, wrong user credentials or user does not exist')
            return redirect('login')


    return render(request, 'todoapp/login.html', {})

@login_required
def DeleteTask(request, id):
    get_todo = todo.objects.get(user=request.user, id=id)
    get_todo.delete()
    return redirect('home-page')

@login_required
def Update(request, id):
    get_todo = todo.objects.get(user=request.user, id=id)
    get_todo.status = not get_todo.status
    get_todo.save()
    return redirect('home-page')

def Edit(request, id):
    get_todo = todo.objects.get(user=request.user, id=id)
    if request.method=='POST':
        task=request.POST.get('task')
        get_todo.todo_name=task
        get_todo.save()
        return redirect('home-page')

    
    context = {
        'todo': get_todo
    }
    
    return render(request, 'todoapp/edit.html',context)