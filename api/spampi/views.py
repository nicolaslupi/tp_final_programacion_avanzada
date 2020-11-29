""" SpamPi Views """

from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Mail
from .serializers import MailSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import sys
cwd = os.path.join(
        os.getcwd(),
        "spampi"
    )
sys.path.append(cwd)
import modelo_spam  # noqa
mod_trained = modelo_spam.ModeloSpam.load_spam_model(in_path=cwd)

@api_view(['POST'])
def process_email(request):
    if request.method == 'POST': # Se lo llama asi: requests.post(url=.../process_email/, json={'text': mail}), o desde el browser...
        data = request.data
        mail = data['text'] # Extraemos el mail de la data parseada
        result = mod_trained.predict_email( mail ) # Predecimos si es Spam o Ham
        result = "Spam" if result==1 else "Ham"

        response = {'result':result, 'status':'OK'} # Esta es la respuesta
        data = {'text':mail, 'result':result, 'status':'OK'} # Esto es lo que se guarda en la base
        serializer = MailSerializer(data = data)
        if serializer.is_valid(): # Siempre va a ser valida porque la construí en la línea de arriba...
            serializer.save()
            return Response(response, status=status.HTTP_200_OK) # Al request le aplican r.json() y visualizan esta respuesta
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def history(request, N_EMAILS):
    if request.method == 'GET':
        # Falta implementar que traiga solo los del usuario actual, pero primero hay que implementar a los usuarios...
        mails = Mail.objects.order_by("-created_at")[:N_EMAILS] # El menos adelante para que traiga los últimos
        serializer = MailSerializer( mails, many=True )
        return Response( serializer.data )