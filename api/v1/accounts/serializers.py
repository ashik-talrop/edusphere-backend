from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from accounts.models import *

class UserProfileSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    email = serializers.EmailField(required=True)
    school_name = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())

    class Meta:
        model = UserProfile
        fields = ['password', 'name', 'student_class', 'email', 'image', 'school_name']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')

        # Create the User instance
        user = User.objects.create(username=email, email=email)  # Use email as the username
        user.set_password(password)
        user.save()

        # Create the UserProfile instance
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile
    

class UserSerializer(serializers.ModelSerializer):
    school_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')  

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'name',
            'image',
            'school_name',
            'email',  
        ]

    def get_school_name(self, obj):
        return obj.school_name.name
