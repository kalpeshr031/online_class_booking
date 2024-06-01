from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import AvailableTime, Reservation
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

class UserTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'age': 25,
            'role': 'student',
            'subject': 'math',
            'password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        url = reverse('register')
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'phone': '0987654321',
            'age': 24,
            'role': 'teacher',
            'subject': 'science',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(email='jane.doe@example.com').first_name, 'Jane')

    def test_user_login(self):
        url = reverse('login')
        data = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class AvailableTimeTests(APITestCase):

    def setUp(self):
        self.teacher_data = {
            'first_name': 'Teacher',
            'last_name': 'One',
            'email': 'teacher.one@example.com',
            'phone': '1234567890',
            'age': 30,
            'role': 'teacher',
            'subject': 'math',
            'password': 'password123'
        }
        self.teacher = User.objects.create_user(**self.teacher_data)
        self.client.force_authenticate(user=self.teacher)

    def test_create_available_time(self):
        url = reverse('available-times')
        start_time = timezone.now() + timedelta(days=1, hours=1)
        end_time = start_time + timedelta(hours=1)
        data = {
            'teacher': self.teacher.id,
            'start_time': start_time,
            'end_time': end_time
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AvailableTime.objects.count(), 1)
        self.assertEqual(AvailableTime.objects.get().teacher, self.teacher)

    def test_list_available_times(self):
        AvailableTime.objects.create(
            teacher=self.teacher,
            start_time=timezone.now() + timedelta(days=1, hours=1),
            end_time=timezone.now() + timedelta(days=1, hours=2)
        )
        url = reverse('available-times')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class ReservationTests(APITestCase):

    def setUp(self):
        self.student_data = {
            'first_name': 'Student',
            'last_name': 'One',
            'email': 'student.one@example.com',
            'phone': '1234567890',
            'age': 20,
            'role': 'student',
            'subject': 'math',
            'password': 'password123'
        }
        self.teacher_data = {
            'first_name': 'Teacher',
            'last_name': 'One',
            'email': 'teacher.one@example.com',
            'phone': '1234567890',
            'age': 30,
            'role': 'teacher',
            'subject': 'math',
            'password': 'password123'
        }
        self.student = User.objects.create_user(**self.student_data)
        self.teacher = User.objects.create_user(**self.teacher_data)
        self.available_time = AvailableTime.objects.create(
            teacher=self.teacher,
            start_time=timezone.now() + timedelta(days=1, hours=1),
            end_time=timezone.now() + timedelta(days=1, hours=2)
        )
        self.client.force_authenticate(user=self.student)

    def test_create_reservation(self):
        url = reverse('reservations')
        data = {
            'available_time': self.available_time.id,
            'reserved_time': timezone.now()
        }
        response = self.client.post(url, data, format='json')
        print(response.content)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.get().student, self.student)


    def test_list_reservations(self):
        Reservation.objects.create(
            student=self.student,
            available_time=self.available_time,
            reserved_time=timezone.now()
        )
        url = reverse('reservations')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class TeacherReservationsViewTests(APITestCase):

    def setUp(self):
        self.teacher_data = {
            'first_name': 'Teacher',
            'last_name': 'One',
            'email': 'teacher.one@example.com',
            'phone': '1234567890',
            'age': 30,
            'role': 'teacher',
            'subject': 'math',
            'password': 'password123'
        }
        self.student_data = {
            'first_name': 'Student',
            'last_name': 'One',
            'email': 'student.one@example.com',
            'phone': '1234567890',
            'age': 20,
            'role': 'student',
            'subject': 'math',
            'password': 'password123'
        }
        self.teacher = User.objects.create_user(**self.teacher_data)
        self.student = User.objects.create_user(**self.student_data)
        self.available_time = AvailableTime.objects.create(
            teacher=self.teacher,
            start_time=timezone.now() + timedelta(days=1, hours=1),
            end_time=timezone.now() + timedelta(days=1, hours=2)
        )
        self.reservation = Reservation.objects.create(
            student=self.student,
            available_time=self.available_time,
            reserved_time=timezone.now()
        )
        self.client.force_authenticate(user=self.teacher)

    def test_teacher_can_view_reservations(self):
        url = reverse('teacher-reservations')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.student.id)

    def test_non_teacher_cannot_view_reservations(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('teacher-reservations')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_view_reservations(self):
        self.client.logout()
        url = reverse('teacher-reservations')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
