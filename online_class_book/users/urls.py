from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('available-times/', AvailableTimeView.as_view(), name='available-times'),
    path('reserve-slot/', ReservationView.as_view(), name='reservations'),
    path('reserve-student/', ReservedStudentsView.as_view(), name='teacher-reservations'),
]



    # "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzI4MTA5NCwiaWF0IjoxNzE3MTk0Njk0LCJqdGkiOiIwY2ZjM2I2MTc3MDk0ZmNjODBkMDY0NjBmNzk5NjdkOCIsInVzZXJfaWQiOjJ9.lBCOuy9gPawbYF_Tj6sdONu52Mjb0iVu6J_EBbWtof4",
    # "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3NjI2Njk0LCJpYXQiOjE3MTcxOTQ2OTQsImp0aSI6ImZlYWFjY2JhZTQxOTQ2YmFiOWU4OGJlZTA4ZTI3ZTE0IiwidXNlcl9pZCI6Mn0.uaNsJa9Rlm_wWBIozssh1eXoFkeDIzADU9rbmcjBmCc"