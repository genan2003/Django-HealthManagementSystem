from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from django.db import models
from django.utils import timezone


class Pacient(AbstractBaseUser):
    Nume = models.CharField(max_length=255)
    Prenume = models.CharField(max_length=255)
    CNP = models.CharField(max_length=13, unique=True)
    Parafa_medic_de_familie = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    oras = models.CharField(max_length=255, default="oras")

    USERNAME_FIELD = 'CNP'
    REQUIRED_FIELDS = ['Nume', 'Prenume', 'Parafa_medic_de_familie', 'email']

    def __str__(self):
        return self.CNP


class Medic(AbstractBaseUser):
    Nume = models.CharField(max_length=255)
    Prenume = models.CharField(max_length=255)
    CNP = models.CharField(max_length=13, unique=True)
    Parafa = models.CharField(max_length=255, unique=True)
    oras = models.CharField(max_length=255, default="oras")
    numar_de_telefon = models.CharField(max_length=10)
    specializare = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'CNP'
    REQUIRED_FIELDS = ['Nume', 'Prenume', 'Parafa', 'numar_de_telefon', 'specializare', 'email']

    def __str__(self):
        return self.Nume


class Programare(models.Model):
    Id = models.AutoField(primary_key=True)
    Pacient = models.ForeignKey('Pacient', on_delete=models.CASCADE)
    Data = models.DateTimeField(default=timezone.now)
    Permite_reprogramare = models.BooleanField(default=False)
    Descriere = models.TextField()
    parafa_medic = models.CharField(max_length=255, default="parafa_medic")
    aprobat = models.BooleanField(default=False)

    def __str__(self):
        return f'Programare {self.Id} for {self.Pacient}'


class Recomandare(models.Model):
    medic = models.ForeignKey(Medic, on_delete=models.CASCADE)
    programare = models.ForeignKey(Programare, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'Recomandare from {self.medic} to {self.programare.Pacient}'
