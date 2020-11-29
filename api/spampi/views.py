from django.http import HttpResponse
import os
import sys
cwd = os.path.join(
        os.getcwd(),
        "spampi"
    )
sys.path.append(cwd)
import modelo_spam  # noqa
mod_trained = modelo_spam.ModeloSpam.load_spam_model(in_path=cwd)


def process_email(request):
    texto_test = "buy viagara king of nigeria buy"
    result = mod_trained.predict_email(texto_test)
    mail_type = "Spam" if result == 1 else "Ham"
    mesg = f"The email processed is: {mail_type}!"
    return HttpResponse(mesg)
