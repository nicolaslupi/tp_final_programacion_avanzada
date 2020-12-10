""" SpamPi URLs """

from django.contrib import admin
from django.urls import path
from spampi import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api-token-auth/', obtain_jwt_token),
    path(r'quota_info/', views.quota_info.as_view()),
    path(r"process_email", views.process_email.as_view()),
    path(r"history/<int:N_EMAILS>/", views.history.as_view()),
    path(r"get_mails/", views.get_mails.as_view()),
    path(r"get_profiles/", views.get_profiles.as_view()),
    path(r"get_users/", views.get_users.as_view()),
]
