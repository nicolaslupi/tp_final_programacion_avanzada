""" SpamPi URLs """

from django.contrib import admin
from django.urls import path
from spampi import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token),
    path('quota_info/', views.quota_info.as_view()),
    path("process_email/", views.process_email.as_view()),
    path("history/<int:N_EMAILS>/", views.history.as_view()),
]
