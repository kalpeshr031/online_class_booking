from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from rest_framework import generics, serializers, status
from rest_framework.response import Response
from .serializers import AvailableTimeSerializer




User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    # print("queryset:----------",queryset)
    serializer_class = UserSerializer

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        print("refresh Token:--------",refresh)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


# -------- ------------------------           ----------------

class AvailableTimeView(generics.ListCreateAPIView):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeSerializer
    permission_classes = [IsAuthenticated]


# # ----------

def assign_default_time_range(student):
    teachers = CustomUser.objects.filter(role='teacher')[:3]
    if not teachers.exists():
        return None  

    default_teacher = teachers[0]
    default_time_range = AvailableTime.objects.filter(teacher=default_teacher).first()
    if not default_time_range:
        return None  

    # Create a reservation for the student
    reservation = Reservation(student=student, available_time=default_time_range)
    reservation.save()

    return reservation


class ReservationView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        student = self.request.user
        if student.role != 'student':
            raise ValidationError({"detail": "Only students can reserve a time slot."})

        if student.is_active:
            # Active student, proceed with the reservation
            serializer.save(student=student)
        else:
            # Inactive student, assign a default time slot
            reservation = assign_default_time_range(student)
            if reservation:
                return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)
            else:
                raise ValidationError({"detail": "No available time range found."})





class ReservedStudentsView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user.role != 'teacher':
            return Response({"detail": "Only teachers can access this information."}, status=status.HTTP_403_FORBIDDEN)
        
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        teacher = self.request.user
        reservations = Reservation.objects.filter(available_time__teacher=teacher)
        student_ids = reservations.values_list('student_id', flat=True)
        return CustomUser.objects.filter(id__in=student_ids, role='student')
