from django.test import TestCase

# Create your tests here.
import json
from django.utils.http import urlencode
from django.urls import reverse
from django.core import serializers
from rest_framework import status
from rest_framework.test import APITestCase
from autoapi.models import HeroPower

from django.contrib.auth.models import User


class HeroPowerCreateTestCase(APITestCase):
    url = "/api/HeroPower/"

    def setUp(self):
        self.valid_payload = {
            "hero": "mrx",
            "power":"zzz",
            "description":"yyy"
        }
        self.invalid_payload = {
            'name': '',
            'age': 14,
            'color': 'W'
        }

    def test_create_heropower(self):
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(201, response.status_code)
        
    def test_create_bad_heropower(self):
        response = self.client.post(self.url, self.invalid_payload)
        self.assertEqual(400, response.status_code)

    def test_heropower_count(self):
        """
        Test to count heropower
        """
        HeroPower.objects.create(hero="xxx", power="zzz", description="yyy")
        HeroPower.objects.create(hero="xxx2", power="zzz2", description="yyy2")
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)) == HeroPower.objects.count())
    
    def test_heropower_filter(self):
        """
        Test to filter heropower
        """
        
        HeroPower.objects.create(hero="mrx", power="zzz", description="yyy")
        HeroPower.objects.create(hero="xxx2", power="zzz2", description="yyy2")
        HeroPower.objects.create(hero="sm", power="zzz2", description="yyy2")
        
        url = '/api/HeroPower/?hero=mrx&ordering=-id&format=json'
        
        hps = HeroPower.objects.filter(hero="mrx")
        hps_json = serializers.serialize("json", hps)
        response = self.client.get(url)
        """
        hps_json [{
            "model": "autoapi.heropower",
            "pk": 3,
            "fields": {"hero": "sm", "power": "zzz2",
                        "description": "yyy2"}}]
        """
        res = json.loads(response.content)[0]
        res.pop("id", None)
        self.assertDictEqual(res, self.valid_payload)

    def test_heropower_and_filter(self):
        """
        Test to filter heropower
        """
        url = '/api/HeroPower/?hero__in=sm%2C+mrx&ordering=id&format=json'
        
        HeroPower.objects.create(hero="mrx", power="zzz", description="yyy")
        HeroPower.objects.create(hero="xxx2", power="zzz2", description="yyy2")
        HeroPower.objects.create(hero="sm", power="zzz2", description="yyy2")
        
        response = self.client.get(url)
        res_len = len(json.loads(response.content))
        
        self.assertTrue(res_len == 2)
        
        
    def test_heropower_limit(self):
        """
        Test to filter heropower
        """
        url = '/api/HeroPower/?hero=mrx&limit=1&offset=0&ordering=-id&format=json'
        
        HeroPower.objects.create(hero="mrx", power="zzz2", description="yyy2")
        HeroPower.objects.create(hero="mrx", power="zzz3", description="yyy3")
        HeroPower.objects.create(hero="mrx", power="zzz", description="yyy")
        HeroPower.objects.create(hero="XXX", power="zzz3", description="yyy3")
        
        response = self.client.get(url)
        res = json.loads(response.content)["results"][0]
        res.pop("id", None)
        
        self.assertDictEqual(res, self.valid_payload)

