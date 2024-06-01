from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate
from .models import *



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'phone', 'age','role','subject','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        message = f"{user.first_name} {user.last_name} successfully registered."
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("---------Incorrect Credentials---------")


# --------------------     -----------------------    ---------------------------




class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTime
        fields = '__all__'

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")
        
        tomorrow = timezone.now() + timedelta(days=1)
        print("TOMORROW:-------------------",tomorrow)

        if not (start_time.date() == end_time.date() == tomorrow.date()):
            raise serializers.ValidationError("Available time range must be for the next day.")
        
        return data



class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
