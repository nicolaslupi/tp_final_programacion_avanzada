""" SpamPi Models """

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Un objeto 'perfil' con relación 1 a 1 con algún usuario de Django
    Se le agrega el campo Quota
    Es asi: Se va al admin de django --> se crean todos los usuarios que quieras -->
        luego desde el admin vas a perfiles y los asignas a los usuarios, y les podes
        modificar las cuotas desde ahi
    Es bastante rustico, estaria bueno que el perfil se cree automaticamente con el usuario,
        pero esto no se evalua...
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    original_quota = models.IntegerField(default=1000, blank=True)
    quota = models.IntegerField(default=1000)

    def __str__(self):
        return self.user.username


class Mail(models.Model):
    # esto es el mail que manda el usuario
    text = models.TextField()
    # spam o ham
    result = models.CharField(max_length=10)
    # ??? puede que sea para otra cosa?
    status = models.CharField(max_length=10)
    # esto sirve para hacer query de mails mas recientes procesados
    created_at = models.DateTimeField(default=now)

    user = models.ForeignKey(
        User, blank=True, default=None, on_delete=models.CASCADE
    )

    def __str__(self):
        # Para que en el admin se visualice el text de los mails
        return self.text
