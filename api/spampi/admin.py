""" SpamPi Admin """

from django.contrib import admin
from .models import Mail, Profile

admin.site.register(Mail)
admin.site.register(Profile)