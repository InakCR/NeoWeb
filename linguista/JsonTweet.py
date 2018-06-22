# -*- coding: utf-8 -*-
import json

from .conexionBD import ConexionBD
from _datetime import datetime


class JsonTweet(object):
    file = "salida_tweet"
    identificador = -1
    fechaA = " "

    def __init__(self, tweet, perfil, local, date):
        self.tweetO = tweet
        self.perfil = perfil
        self.localizacion = local
        self.fecha = date
        # lista por cada filtro
        self.lexema = []
        self.lema = []
        self.hastag = []
        self.malcomp = []
        self.ciclico = []
        self.diminutivo = []
        # palaba candidata
        self.unk = []

    def get_tweet(self):
        return self.tweetO

    def add_id(self, iden):
        self.identificador = iden

    def add_lexema(self, lex):
        if lex not in self.lexema:
            self.lexema.append(lex)

    def add_lema(self, le):
        if le not in self.lema:
            self.lema.append(le)

    def add_hastag(self, has):
        if has not in self.hastag:
            self.hastag.append(has)

    def add_malcomp(self, malcomp):
        if malcomp not in self.malcomp:
            self.malcomp.append(malcomp)

    def add_ciclico(self, cicli):
        if cicli not in self.ciclico:
            self.ciclico.append(cicli)

    def add_ito(self, ito):
        if ito not in self.diminutivo:
            self.diminutivo.append(ito)

    def add_unk(self, palabra):
        if palabra not in self.unk:
            self.unk.append(palabra)

    def tojson(self) -> object:
        self.fechaA = str(datetime.now())

        def jdefault(o):
            return o.__dict__

        with open(self.file + ".json", mode='a', encoding="utf8") as out:
            out.write(json.dumps(self, default=jdefault, ensure_ascii=False) + '\r')

        # PUT en ElasticSearch
        conex = ConexionBD()
        info = conex.put_tweet(self.identificador, json.dumps(self, default=jdefault, ensure_ascii=False))

        with open("info", mode='a', encoding="utf8") as out:
            out.write(json.dumps(info))
            out.write('\r')

    def put_admitido(self) -> object:
        self.fechaA = str(datetime.now())

        def jdefault(o):
            return o.__dict__

        with open("admitidos.json", mode='a', encoding="utf8") as out:
            out.write(json.dumps(self, default=jdefault, ensure_ascii=False) + '\r')

        conex = ConexionBD()
        conex.put_ads(json.dumps(self, default=jdefault, ensure_ascii=False))

    def put_descartado(self) -> object:
        self.fechaA = str(datetime.now())

        def jdefault(o):
            return o.__dict__

        with open("descartados.json", mode='a', encoding="utf8") as out:
            out.write(json.dumps(self, default=jdefault, ensure_ascii=False) + '\r')

        conex = ConexionBD()
        conex.put_disc(json.dumps(self, default=jdefault, ensure_ascii=False))
