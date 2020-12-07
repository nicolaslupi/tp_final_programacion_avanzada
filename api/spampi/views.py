""" SpamPi Views """

from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Mail, Profile
from django.contrib.auth.models import User
from .serializers import MailSerializer, ProfileSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import os
import sys
cwd = os.path.join(
        os.getcwd(),
        "spampi"
    )
sys.path.append(cwd)
import modelo_spam  # noqa
mod_trained = modelo_spam.ModeloSpam.load_spam_model(in_path=cwd)


class quota_info(APIView):
    """
    Toma el usuario actual y se fija cuánto le queda...
    """
    def get(self, request):
        usuario = request.user
        perfil = Profile.objects.get(user=usuario)
        disponibles = perfil.quota
        procesados = perfil.original_quota - disponibles
        response = {
            'procesados': procesados,
            'disponibles': disponibles
        }
        return Response(response, status=status.HTTP_200_OK)


class process_email(APIView):
    """
    Se le pasa un mail, lo clasifica y resta una quota, a menos que no me queden mas...
    """
    def post(self, request):
        data = request.data
        # Extraemos el mail de la data parseada
        mail = data['text']
        # Predecimos si es Spam o Ham
        result = mod_trained.predict_email(mail)
        result = "Spam" if result == 1 else "Ham"
        # Esta es la respuesta
        response = {'result': result, 'status': 'OK'}
        # Esto es lo que se guarda en la base
        data = {'text': mail, 'result': result, 'status': 'OK'}
        serializer = MailSerializer(data=data)
        # Siempre va a ser valida porque la construí en la línea de arriba...
        if serializer.is_valid():
            # Restamos un mail de la quota al perfil que sea
            usuario = request.user
            perfil = Profile.objects.get(user=usuario)
            quota = perfil.quota
            if quota > 0:
                perfil.quota -= 1
                perfil.save()
                # Guardamos con el perfil
                serializer.save(user=usuario)
                # Al request le aplican r.json() y visualizan esta respuesta
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {'result': 'fail', 'message': 'No quota left'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class history(APIView):
    """
    Trae los últimos N_mails del usuario actual...
    """
    def get(self, request, N_EMAILS):
        usuario = request.user
        # El menos adelante para que traiga los últimos
        mails = Mail.objects.filter(
            user=usuario
            ).order_by("-created_at")[:N_EMAILS]
        serializer = MailSerializer(mails, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class get_mails(APIView):
    """
    Trae todos los mails cargados, solo si soy superuser
    """
    def get(self, request):
        if request.user.is_superuser:
            mails = Mail.objects.all()
            serializer = MailSerializer(mails, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            response = {'result': 'fail', 'message': 'Not a superuser'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class get_profiles(APIView):
    """
    Trae los perfiles de los usuarios, si soy superuser
    """
    def get(self, request):
        if request.user.is_superuser:
            profiles = Profile.objects.all()
            serializer = ProfileSerializer(profiles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            response = {'result': 'fail', 'message': 'Not a superuser'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class get_users(APIView):
    """
    Trae los perfiles de los usuarios, si soy superuser
    """
    def get(self, request):
        if request.user.is_superuser:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            response = {'result': 'fail', 'message': 'Not a superuser'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
