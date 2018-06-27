# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch


class ConexionBD:
    INDEX_TWEETS = "tweets"
    INDEX_DISC = "descartados"
    INDEX_ADS = "admitidos"
    TYPE = "tweet"

    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def crear(self):
        self.es.indices.create(index=self.INDEX_TWEETS, ignore=400)
        self.es.indices.create(index=self.INDEX_ADS, ignore=400)
        self.es.indices.create(index=self.INDEX_DISC, ignore=400)

    def put_tweet(self, iden, text):
        info = self.es.index(index=self.INDEX_TWEETS, doc_type=self.TYPE, id=iden, body=text)
        return info

    def put_ads(self, text):
        self.es.index(index=self.INDEX_ADS, doc_type=self.TYPE, body=text)

    def put_disc(self, text):
        self.es.index(index=self.INDEX_DISC, doc_type=self.TYPE, body=text)

    def exist_ad(self, cand):
        hits = self.get_neo(cand)
        if not hits:
            return False
        return True

    def exist_disc(self, cand):
        hits = self.get_disc(cand)
        if not hits:
            return False
        return True

    def get_nc(self):
        query = {"query": {"match_all": {}}}

        return self.es.count(index=self.INDEX_ADS, doc_type=self.TYPE, body=query)

    def ger_ne(self):

        hits = self.get_tweet()
        neos = set()

        for hit in hits:
            neos.add(hit['_source']['unk'])

        return len(neos)

    def get_tweet(self, disc=True, ads=True):
        query = {"query": {"match_all": {}}}
        lista = ["tweetO", "perfil", "localizacion", "fecha", "unk"]

        res = self.es.search(index=self.INDEX_TWEETS, doc_type=self.TYPE, body=query, _source=lista, _source_include=lista)

        hits = res['hits']['hits']
        if not disc:
            pass
        if not ads:
            pass
        return hits

    def get_ads(self):
        query = {"query": {"match_all": {}}}
        lista = ["tweetO", "perfil", "localizacion", "fecha", "unk"]

        res = self.es.search(index=self.INDEX_ADS, doc_type=self.TYPE, body=query, _source=lista, _source_include=lista)
        hits = res['hits']['hits']

        return hits

    def get_neo(self, neo):
        query = {"query": {"match": {"unk": neo}}}
        lista = ["tweetO", "perfil", "localizacion", "fecha", "unk"]

        res = self.es.search(index=self.INDEX_ADS, doc_type=self.TYPE, body=query, _source=lista, _source_include=lista)
        hits = res['hits']['hits']

        return hits

    def get_disc(self, disc):
        query = {"query": {"match": {"unk": disc}}}
        lista = ["tweetO", "perfil", "localizacion", "fecha", "unk"]

        res = self.es.search(index=self.INDEX_DISC, doc_type=self.TYPE, body=query, _source=lista, _source_include=lista)
        hits = res['hits']['hits']

        return hits

    def get_cand(self, cand):
        query = {"query": {"match": {"unk": cand}}}
        lista = ["tweetO", "perfil", "localizacion", "fecha", "unk"]

        res = self.es.search(index=self.INDEX_TWEETS, doc_type=self.TYPE, body=query, _source=lista, _source_include=lista)
        hits = res['hits']['hits']

        return hits

    def get_neo_by_letter(self, letter):
        query = {"query": {"match_phrase_prefix": {"unk": {"query": letter}}}}
        lista = ["tweetO", "perfil", "localizacion", "fecha", "unk"]

        res = self.es.search(index=self.INDEX_ADS, doc_type=self.TYPE, body=query, _source=lista, _source_include=lista)
        hits = res['hits']['hits']

        return hits

    def get_neo_by_date(self,date1,date2):
        query = {
            "query": {
                "range": {
                    "fecha": {
                        "gte": "2013",
                        "lte": "2018"
                    }
                }

            }, "sort": {"fecha": "asc"},
            "size": 10}
        lista = ["tweetO", "perfil", "localizacion", "fecha", "unk"]

        res = self.es.search(index=self.INDEX_ADS, doc_type=self.TYPE, body=query, _source=lista, _source_include=lista)
        hits = res['hits']['hits']

        return hits

    def get_ads_lasts(self):
        query = {"query": {"match_all": {}}}
        lista = ["tweetO", "perfil", "localizacion", "fecha", "unk"]

        res = self.es.search(index=self.INDEX_ADS, doc_type=self.TYPE, body=query, _source=lista, _source_include=lista)
        hits = res['hits']['hits']

        if not hits:
            return hits

        query = {"query": {"match_all": {}}, "sort": {"fechaA.keyword": "desc"}, "size": 5}
        res = self.es.search(index=self.INDEX_ADS, doc_type=self.TYPE, body=query, _source=lista, _source_include=lista)
        hits = res['hits']['hits']
        return hits

    def delete_ad(self, neo):
        query = {"query": {"match": {"unk": neo}}}

        self.es.delete_by_query(index=self.INDEX_ADS, doc_type=self.TYPE, body=query)

    def delete_disc(self, neo):
        query = {"query": {"match": {"unk": neo}}}

        self.es.delete_by_query(index=self.INDEX_DISC, doc_type=self.TYPE, body=query)
