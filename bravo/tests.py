from django.test import TestCase
from rest_framework import status
import json

class Teste(TestCase):
    def test_usd_to_brl(self):
        response = self.client.get('/', {
            'from': 'USD',
            'amount': 1,
            'to': 'BRL',
        },)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_parameters_error(self):
        response = self.client.get("/" ,{
            
        },)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_amount_error(self):
        response = self.client.get('/', {
            'from': 'BRL',
            'amount': "amount",
            'to': 'ETH',
        },)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_from_error(self):
        response = self.client.get('/', {
            'amount': 123.45,
            'to': 'ETH',
        },)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_to_error(self):
        response = self.client.get('/', {
            'from': 'BRL',
            'amount': 123,
        },)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)