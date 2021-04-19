from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from app_one.models import UserInfo, StudentInfo, TeacherInfo
from django.contrib import messages
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            user_instance = UserInfo.objects.get(user = user)
            role = user_instance.role
            if role == False:
                print('student')
                return redirect('home_url')
            elif role == True:
                print('teacher')
                return redirect('home_url')
            else:
                messages.error(request, 'Invalid login')
                return redirect('login_url')
        else:
            messages.error(request, 'Invalid login credentials')
    
    return render(request, 'login.html')


@login_required
def home_view(request):
    user_instance = UserInfo.objects.get(user = request.user)
    if user_instance.role == False:
        student = StudentInfo.objects.get(admin = user_instance)
        name = student.name
    if user_instance.role == True:
        teacher = TeacherInfo.objects.get(admin = user_instance)
        name = teacher.name
    return render(request, 'home.html', {'name' : name})

def developers_view(request):
    return render(request, 'developers.html')

def about_view(request):
    return render(request, 'about.html')