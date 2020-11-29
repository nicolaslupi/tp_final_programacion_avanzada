""" SpamPi URLs """

from django.contrib import admin
from django.urls import path
from spampi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("process_email/", views.process_email)
]
