# -*- coding: utf-8 -*-
import requests


class Grampal:
    service_in = 'http://leptis.lllf.uam.es/api/grampal/general/'
    
    def __init__(self, service=None):
        if service is not None:
            self.service_in = service
    
    def analiza_post(self, phrase):
        return requests.get(self.service_in+phrase)

    def analiza_get(self, phrase):
        return requests.post(self.service_in, data={'texto': phrase})

    def analiza(self, phrase):
        return self.analiza_get(phrase)
