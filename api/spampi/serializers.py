""" SpamPi Serializers """
from rest_framework import serializers
from .models import Mail, Profile
from django.contrib.auth.models import User

class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'