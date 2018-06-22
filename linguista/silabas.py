# -*- coding: utf-8 -*-


class Silabas:

    def __init__(self):
        self.dic = {}
        with open("./datos/silabaslimpio.txt", mode='r', encoding="utf8") as out:
            for sil in out:
                sil = sil.strip("\n")
                if sil[0] in self.dic:
                    self.dic[sil[0]].append(sil)
                else:
                    self.dic[sil[0]] = [sil]
