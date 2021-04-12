from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    role_types = ((False, "Student"), (True, "Teacher"))
    role = models.BooleanField(choices = role_types, default = False)

    def __str__(self):
        return self.user.username

class StudentInfo(models.Model):
    admin = models.OneToOneField(UserInfo, on_delete = models.CASCADE)
    name = models.CharField(default = "default name",max_length = 20)
    address = models.CharField(default = "default address",max_length = 100, blank = True)
    age = models.IntegerField(default = 0)
    gender_types = (("M", "Male"), ("F", "Female"))
    gender = models.CharField(choices = gender_types, max_length = 1, null = True, blank = True)
    contact = models.CharField(max_length = 10, null = True, blank = True)
    emailID = models.EmailField(max_length = 50, null = True, blank = True)

    def __str__(self):
        return str(self.admin.user.username)



class TeacherInfo(models.Model):
    admin = models.OneToOneField(UserInfo, on_delete = models.CASCADE)
    name = models.CharField(default = "default name",max_length = 20)
    address = models.CharField(default = "default address",max_length = 100, blank = True)
    age = models.IntegerField(default = 0)
    gender_types = (("M", "Male"), ("F", "Female"))
    gender = models.CharField(choices = gender_types, max_length = 1, null = True, blank = True)
    contact = models.CharField(max_length = 10, null = True, blank = True)
    emailID = models.EmailField(max_length = 50, null = True, blank = True)

    def __str__(self):
        return str(self.admin.user.username)

class Course(models.Model):
    course_name = models.CharField(max_length = 50)
    course_id = models.CharField(max_length = 10, primary_key = True)

    def __str__(self):
        return str(self.course_id)

class Mark(models.Model):
    student_id = models.ForeignKey(StudentInfo, on_delete = models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
    quiz1 = models.FloatField(default = 0)
    quiz2 = models.FloatField(default = 0)
    mst = models.FloatField(default = 0)
    est = models.FloatField(default = 0)

    def __str__(self):
        return str(self.student_id.admin.user.username + " " + self.course_id.course_id)

class Attendance(models.Model):
    student_id = models.ForeignKey(StudentInfo, on_delete = models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
    date = models.DateField()
    status_choices = ((True, "Present"), (False, "Absent"))
    status = models.BooleanField(choices = status_choices)

    def __str__(self):
        return str(self.student_id.admin.user.username + " " + self.course_id.course_id)

class Course_taken(models.Model):
    student_id = models.ForeignKey(StudentInfo, on_delete = models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
 
    def __str__(self):
        return str(self.student_id.admin.user.username + " " + self.course_id.course_id)


class Course_teaching(models.Model):
    teacher_id = models.ForeignKey(TeacherInfo, on_delete = models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.teacher_id.admin.user.username + " " + self.course_id.course_id)


@receiver(post_save, sender = UserInfo) 
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == False:
            StudentInfo.objects.create(admin = instance)
        if instance.role == True:
            TeacherInfo.objects.create(admin = instance)

@receiver(post_save, sender = UserInfo)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == False:
        instance.studentinfo.save()
    if instance.role == True:
        instance.teacherinfo.save()




