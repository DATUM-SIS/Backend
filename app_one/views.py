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

@login_required
def profile_view(request):
    admin = UserInfo.objects.get(user = request.user)
    if admin.role == False:
        student = StudentInfo.objects.get(admin = admin)
        profile_details = {'name' : student.name, 'address' : student.address, 'age' : student.age, 'gender' : student.gender, 'contact' : student.contact, 'emailid' : student.emailID}
        return render(request, 'profile.html', profile_details)
    else:
        teacher = TeacherInfo.objects.get(admin = admin)
        profile_details = {'name' : teacher.name, 'address' : teacher.address, 'age' : teacher.age, 'gender' : teacher.gender, 'contact' : teacher.contact, 'emailid' : teacher.emailID}
        return render(request, 'profile.html', profile_details)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login_url')

def developers_view(request):
    return render(request, 'developers.html')

def about_view(request):
    return render(request, 'about.html')

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        age = int(request.POST.get('age'))
        contact = request.POST.get('contact')
        sex = request.POST.get('sex')
        admin = UserInfo.objects.get(user = request.user)
        if admin.role == False:
            student = StudentInfo.objects.get(admin = admin)
            student.name = name
            student.emailID = email
            student.address = address
            student.age = age
            student.contact = contact
            student.gender = sex
            student.save()
        else:
            teacher = TeacherInfo.objects.get(admin = admin)
            teacher.name = name
            teacher.emailID = email
            teacher.address = address
            teacher.age = age
            teacher.contact = contact
            teacher.gender = sex
            teacher.save()
        return redirect('profile_url')
        print('profile updated successfully')
    return render(request, 'edit_profile.html')