""" SpamPi Views """

from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Mail
from .serializers import MailSerializer
from django.views.decorators.csrf import csrf_exempt
import os
import sys
cwd = os.path.join(
        os.getcwd(),
        "spampi"
    )
sys.path.append(cwd)
import modelo_spam  # noqa
mod_trained = modelo_spam.ModeloSpam.load_spam_model(in_path=cwd)

@csrf_exempt
def process_email(request):
    if request.method == 'POST':
        data = JSONParser().parse(request) # El pedido debe ser: requests.post(url=.../process_email/, json={'text': mail }) (en mail va el mail)
        mail = data['text'] # Extraemos el mail de la data parseada
        result = mod_trained.predict_email( mail ) # Predecimos si es Spam o Ham
        result = "Spam" if result==1 else "Ham"

        response = {'result':result, 'status':'OK'} # Esta es la respuesta
        data = {'text':mail, 'result':result, 'status':'OK'} # Esto es lo que se guarda en la base
        serializer = MailSerializer(data = data)
        if serializer.is_valid(): # Siempre va a ser valida porque la construí en la línea de arriba...
            serializer.save()
            return JsonResponse(response, status=201) # Al request le aplican r.json() y visualizan esta respuesta
        else:
            return JsonResponse(serializer.errors, status=400)
    
    
    