from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
# create all models



ROLE_CHOICES = (
    ('student', 'Student'),
    ('teacher', 'Teacher'),
)

SUBJECT_CHOICES = [
        ('math', 'Mathematics'),
        ('science', 'Science'),
        ('history', 'History'),
        # Add more subject choices as needed
    ]

class CustomUser(AbstractUser):

    username = None
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)


    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()



    def __str__(self):
        return self.email
    


# ---------------------------------------------------------------------------------------------------------------------------


class AvailableTime(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

   

    def __str__(self):
        return f'{self.teacher.username}: {self.start_time} - {self.end_time}'


class Reservation(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    available_time = models.ForeignKey(AvailableTime, on_delete=models.CASCADE)
    reserved_starttime = models.DateTimeField()
    reserved_endtime = models.DateTimeField()


    def __str__(self):
        return f'{self.student.username} reserved {self.reserved_time}'
