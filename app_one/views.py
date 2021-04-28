from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from app_one.models import UserInfo, StudentInfo, TeacherInfo, Course_taken, Course_teaching, Mark, Attendance, User, Course
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
                return redirect('home_url')
            elif role == True:
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


@login_required
def course_view(request):
    admin = UserInfo.objects.get(user = request.user)
    if request.method == 'POST':
        user_demand = request.POST.get('user_demand')
        action_and_id = user_demand.split(',')
        request.session['cid'] = action_and_id[1]
        if action_and_id[0]  == 'marks':
            if admin.role == False:
                return redirect('student_marks_url')
            else :
                return redirect('teacher_marks_url')
        else :
            if admin.role == False:
                return redirect('student_attendance_url')
            else :
                return redirect('teacher_attendance_url')
    lst = []
    if admin.role == False:
        student = StudentInfo.objects.get(admin = admin)
        courses = Course_taken.objects.filter(student_id = student)
        for course in courses:
            lst.append((course.course_id.course_id, course.course_id.course_name))
            
    else:
        teacher = TeacherInfo.objects.get(admin = admin)
        courses = Course_teaching.objects.filter(teacher_id = teacher)
        for course in courses:
            lst.append((course.course_id.course_id, course.course_id.course_name))
    return render(request, 'course.html', {'courses' : lst})

@login_required
def student_marks_view(request):
    admin = UserInfo.objects.get(user = request.user)
    student = StudentInfo.objects.get(admin = admin)
    marks_obj = Mark.objects.filter(student_id = student, course_id = request.session['cid'])
    context_dict = {}
    for marks in marks_obj:
        context_dict['q1'] = marks.quiz1
        context_dict['q2'] = marks.quiz2
        context_dict['mst'] = marks.mst
        context_dict['est'] = marks.est
        context_dict['percentage'] = int((context_dict['q1'] + context_dict['q2'] + context_dict['mst'] + context_dict['est']))
    return render(request, 'student_marks.html', context_dict)

@login_required
def student_attendance_view(request):
    admin = UserInfo.objects.get(user = request.user)
    student = StudentInfo.objects.get(admin = admin)
    lst = []
    count_total = 0
    count_present = 0
    attendance_obj = Attendance.objects.filter(student_id = student, course_id = request.session['cid'])
    for i in attendance_obj:
        count_total += 1
        if i.status == True:
            count_present += 1
            lst.append((i.date, 'Present'))
        else:
            lst.append((i.date, 'Absent'))
    percentage = int((count_present*100)/count_total)
        
    return render(request, 'student_attendance.html', {'attendance' : lst, 'percentage' : percentage})


@login_required
def teacher_attendance_view(request):
    admin = UserInfo.objects.get(user = request.user)
    teacher = TeacherInfo.objects.get(admin = admin)
    attendance_obj = Attendance.objects.filter(course_id = request.session['cid'])
    lst = []
    count = 0
    for i in attendance_obj:
        if i.date not in lst:
            lst.append(i.date)
            count += 1
    return render(request, 'teacher_attendance.html', {'dates' : lst, 'count' : count})


@login_required
def mark_attendance_view(request):
    students_list = Attendance.objects.filter(course_id = request.session['cid'])
    lst = []
    for i in students_list:
        uname = i.student_id.admin.user.username
        if uname not in lst:
            lst.append(uname)
    if request.method == 'POST':
        for i in lst:
            user = User.objects.get(username = i)
            userinfo = UserInfo.objects.get(user = user)
            studentinfo = StudentInfo.objects.get(admin = userinfo)
            course_instance = Course.objects.get(course_id = request.session['cid'])
            if request.POST.get(i) is not None:
                attendance_obj = Attendance(date = request.POST.get('date'), course_id = course_instance, student_id = studentinfo, status = True)
            else:
                attendance_obj = Attendance(date = request.POST.get('date'), course_id = course_instance, student_id = studentinfo, status = False)
            attendance_obj.save()
        return redirect('teacher_attendance_url')
    return render(request, 'mark_attendance.html', {'students' : lst})

def teacher_marks_view(request):
    return render(request, 'teacher_marks.html')