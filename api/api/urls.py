""" SpamPi URLs """

from django.contrib import admin
from django.urls import path
from spampi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quota_info/', views.quota_info.as_view()),
    path("process_email/", views.process_email.as_view()),
    path("history/<int:N_EMAILS>/", views.history.as_view()),
]
