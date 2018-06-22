from django.db import models


class User:
    userName = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.userName


class Neo:
    lexema = models.CharField()
    tweet = models.TextField()
    date = models.DateField()
    bio = models.TextField()
    local = models.TextField()

    def __str__(self):
        return self.lexema


class Candidato:
    def __init__(self):
        self.ads = False
        self.disc = False

    lexema = models.CharField()
    tweet = models.TextField()
    date = models.TextField()
    bio = models.TextField()
    local = models.TextField()
    ads = models.BooleanField()
    disc = models.BooleanField()

    def __str__(self):
        return self.lexema
