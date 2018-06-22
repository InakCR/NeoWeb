# -*- coding: utf-8 -*-
import re
import unicodedata
import json
# from detector import Detector
from .JsonTweet import JsonTweet
from .grampal import Grampal
from .silabas import Silabas
from subprocess import *


class Extract:

    def __init__(self, lang="spanish"):
        self.lang = lang
        self.tweet = JsonTweet("Null", "Null", "Null", "Null")
        self.silabas = Silabas()

    def extraer(self, file):
        with open(file, mode='r', encoding="utf8") as fo:
            for tweetJ in fo:
                if self.lector_json(tweetJ):

                    line = self.tweet.get_tweet()

                    if self.retweet(line):
                        # Posible perdida de informacion
                        # Patrones de limpiar
                        line = self.patron_arroba(line)
                        line = self.patron_http(line)
                        line = self.patron_html(line)
                        line = self.patron_nromanos(line)
                        line = self.elimina_saltos(line)
                        line = line.lower()
                        line = self.eliminar_hastag(line)
                        line = self.patron_triplicadas(line)
                        # line = self.patron_cliticos(line)
                        # Idioma
                        # if self.deteccion_idioma(line):
                        # Filtros a nivel de palabras ( desconocidas o no)
                        palabras_g = self.patron_lexemas(line)
                        self.grampal(palabras_g)
                        self.tweet.tojson()

    def grampal(self, palabras):
        unk = "/UNKN"
        lemas = ["/N", "/V", "/ADJ"]
        palabras_gp = []
        p_unks = []
        g = Grampal()
        data = g.analiza_get(palabras)

        for linea in data.text.splitlines():  # Analisis de salid de Grampal
            palabras_gp.append(linea)
            if unk in linea:  # Busqueda de  cada UNKNOW
                u = linea.split('/')[0]
                ad, bi = self.patron_itos(u)
                ad, bc = self.patron_cliticos(ad)
                if bi or bc:  # Nueva busqueda si es corregida la palabra
                    gran = g.analiza_get(ad)
                    if unk in gran:
                        u = self.elimina_tildes(u)
                        if self.composicion_silabas(u):
                            self.tweet.add_unk(u)
                            if bi:
                                self.tweet.add_ito(u)
                            if bc:
                                self.tweet.add_ciclico(u)
                        else:
                            self.tweet.add_malcomp(u)
                    else:
                        self.tweet.add_lema(ad)
                else:
                    # Si no es corregida
                    # Añadimos las palabas unk por is tiene sentido juntas (Nombres)
                    p_unks.append(u)
            # No UNKNOWS
            else:
                for lema in lemas:
                    if lema in linea:
                        self.tweet.add_lema(linea.split('/')[0])

        # Miramos todos los unks encontrados en el tweet
        # Eliminamos los Names de JRC
        found, names = self.busca_jrc_names(p_unks)
        if found:
            for n in names:
                if n in p_unks:
                    p_unks.remove(n)
        for u in p_unks:
            if self.composicion_silabas(u):
                self.tweet.add_unk(u)
            else:
                self.tweet.add_malcomp(u)

        # self.salida("salida.txt", palabras_gp)
        return palabras_gp

    def patron_itos(self, unk):
        diminutivos = ["ito$", "ita$", "ico$", "ica$", "illo$", "illa$", "ico$", "ica$", "ucho$", "ucha$", "ín$",
                       "ina$", "uelo$", "uela$", "ete$", "eta$", "uco$", "uca$"]
        if len(unk) > 5:
            for dim in diminutivos:
                if re.search(dim, unk):
                    return re.sub(dim, dim[len(dim) - 2], unk), True
        return unk, False

    def patron_cliticos(self, unk):

        comp_su = ["lo", "la", "le", "les"]
        comp_pre = ["me", "te", "se"]

        if len(unk) > 5:
            for comp1 in comp_pre:
                for comp2 in comp_su:
                    exp = comp1 + comp2 + "$"
                    if re.search(exp, unk):
                        return re.sub(exp, "", unk), True
        return unk, False

    def composicion_silabas(self, unk):
        i = 1

        if not unk:
            return True

        list_sil = self.silabas.dic.get(unk[0])

        if list_sil is None:
            return False

        cand = unk[0]
        for sil in list_sil:

            if re.match(cand, sil):
                if i < len(unk):
                    cand = cand + unk[i]
                    i += 1
                else:
                    i += 1
                    break

        return self.composicion_silabas(unk[i - 1:])

    def patron_arroba(self, line):
        return self.aplica_patron(re.compile("@([^ ]+|$)"), line, "@")

    def patron_http(self, line):
        return self.aplica_patron(re.compile("http([^ ]+|$)"), line, "http")

    def patron_html(self, line):
        return self.aplica_patron(re.compile('&[^;]*;'), line)

    def patron_nromanos(self, line):
        patron = "(IX|IV|VI{1,3})"
        line = self.aplica_patron(re.compile(patron), line)
        patron = "(XC|XL|LX{1,3})"
        line = self.aplica_patron(re.compile(patron), line)
        patron = "(CM|CD|DC{1,3})"
        line = self.aplica_patron(re.compile(patron), line)
        patron = "(MC{1,3}|MD{1,3}|ML{1,3})"
        return self.aplica_patron(re.compile(patron), line)

    def patron_lexemas(self, line):
        patron = re.compile('((#[a-zñáéíóúü]+|[a-zñáéíóúü]+)[a-zñáéíóúü]+)')
        exps = patron.findall(line)
        palabras_g = " "
        for p in exps:
            self.tweet.add_lexema(p[0])
            palabras_g += str(p[0]) + " "
        return palabras_g

    @staticmethod
    def patron_triplicadas(line):
        patron = re.compile(r'(\w)(\1{3,})')
        return re.sub(patron, r'\1', line)

    @staticmethod
    def aplica_patron(patron, line, replace="", add=None):
        exps = patron.findall(line)
        if add is not None:
            for exp in exps:
                add(exp)
        for exp in exps:
            line = line.replace(replace + exp, " ")
        return line

    def elimina_saltos(self, line):
        line = self.eliminar(line, "\\n\\n")
        line = line.replace('"', ' ')
        return self.eliminar(line, '\\n')

    def eliminar_hastag(self, line):
        patron = re.compile("#([^ ]+|$)")
        exps = patron.findall(line)
        for exp in exps:
            self.tweet.add_hastag(exp)
        return self.eliminar(line, '#')

    @staticmethod
    def eliminar(line, exp):
        return line.replace(exp, ' ')

#   def deteccion_idioma(self, line):
#        d = Detector()
#        return d.detectar(line, self.lang)

    def elimina_tildes(self, s):
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

    def lector_json(self, line):
        d = json.loads(line)
        bio = ""
        local = ""
        if "id" in d:
            iden = (d["id"])
            if "summary" in d["actor"]:
                bio = d["actor"]["summary"]
                if "location" in d["actor"]:
                    if "displayName" in d["actor"]["location"]:
                        local = d["actor"]["location"]["displayName"]
            date = d["postedTime"]
            body = d["body"]
            self.tweet = JsonTweet(body, bio, local, date)
            self.tweet.add_id(iden)
            return True
        else:
            return False

    def busca_jrc_names(self, name):

        def jar_wrapper():
            process = Popen(['java', '-jar', '.\datos\JRCNames.jar', '.\datos\entities.gzip',
                             '.\datos\jrc.txt', 'ES'], stdout=PIPE, stderr=PIPE)
            ret = []
            res = []

            while process.poll() is None:
                line = process.stdout.readline().decode("utf-8")
                if line != '' and line.endswith('\n'):
                    ret.append(line[:-1])

                stdout, stderr = process.communicate()
                ret += stdout.decode("utf-8").split('\n')
                if stderr != '':
                    ret += stderr.decode("utf-8").split('\n')
                ret.remove('')
                for r in ret:
                    if r != '':
                        res.append(r.replace('\r', ''))
                return res

        with open('datos/jrc.txt', mode='w', encoding="utf8") as out:
            for n in name:
                n = self.elimina_tildes(n)
                out.write(n+" ")

        result = jar_wrapper()
        # print(result)
        names = []
        if result is None:
            return False, names
        for n in name:
            if n in result[-1]:
                names.append(n)
        if "found" in result[-1]:
            for n in names:
                if n in name:
                    name.remove(n)
            return True, names
        return False, names

    @staticmethod
    def retweet(line):
        if line.find("RT", 0, 5) is -1:
            return True
        return False

    @staticmethod
    def salida(file, text):
        with open(file, mode='a', encoding="utf8") as out:
            for palabra in text:
                out.write(palabra + '\r')

    def get_lan(self, file):
        l = []
        l.append(self.lang)
        with open(file, mode='a', encoding="utf8") as out:
            for palabra in out:
                l.append(palabra)
        return palabra
