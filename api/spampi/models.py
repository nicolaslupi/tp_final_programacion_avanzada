""" SpamPi Models """

from django.db import models
from django.utils.timezone import now

class Mail(models.Model):
    text = models.TextField()
    result = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=now)
    # Faltaria user = ... para luego filtrar y ver los mails que mande como usuario
    
    def __str__(self):
        return self.text # Para que en el admin se visualice el text de los mails