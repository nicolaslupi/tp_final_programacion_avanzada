from django.shortcuts import render
import os
import sys
cwd = os.path.join(
        os.getcwd(),
        "spampi"
    )
sys.path.append(cwd)
import modelo_spam
# import spampi.modelo_spam as modelo_spam

def process_email(request):
    cwd = os.path.join(
        os.getcwd(),
        "spampi"
    )
    mod_trained = modelo_spam.ModeloSpam.load_spam_model(in_path=cwd)
    texto_test = "buy viagara king of nigeria buy"
    result = mod_trained.predict_email(texto_test)
    print(result)
