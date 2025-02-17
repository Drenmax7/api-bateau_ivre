from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UtilisateurManager(BaseUserManager):
    def create_user(self, mail, mot_de_passe=None, skipHash = False, **extra_fields):
        if not mail:
            raise ValueError("L'email est obligatoire 🦆🔥")

        if skipHash:
            user = self.model(mail=self.normalize_email(mail), password="ceci n'est pas le mot de passe, il est hashe", **extra_fields)
        else:
            user = self.model(mail=self.normalize_email(mail), **extra_fields)
            user.set_password(mot_de_passe)

        user.save(using=self._db)
        return user

    def create_superuser(self, mail, mot_de_passe=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(mail, mot_de_passe, **extra_fields)
    
    def get_by_natural_key(self, mail):
        return self.get(mail=mail)

class Utilisateur(AbstractBaseUser):
    id_utilisateur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    civilite = models.CharField(max_length=50)
    adresse = models.CharField(max_length=200)
    ville = models.CharField(max_length=50)
    pays = models.CharField(max_length=50)
    code_postal = models.CharField(max_length=6, blank=True, null=True)
    telephone = models.CharField(max_length=15)
    complement_adresse = models.CharField(max_length=100, blank=True, null=True)
    premiere_connexion = models.DateTimeField(blank=True, null=True)
    derniere_connexion = models.DateTimeField(blank=True, null=True)

    mail = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "mail"  
    REQUIRED_FIELDS = []  

    objects = UtilisateurManager()