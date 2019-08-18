from django.shortcuts import render
from conversor.models import CurrencyConversion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from rest_framework.throttling import UserRateThrottle
import datetime
from datetime import timedelta 
from decimal import Decimal
from django.utils import timezone


class ConversorMonetario(APIView):
    throttle_classes = [UserRateThrottle]
    def get(self, request, format=None):
        de = request.GET.get('from', False)
        para = request.GET.get('to', False)
        montante = request.GET.get('amount', False)
        try:
            data = {'From': de, 'To': para, 'Amount': montante, 'Price': 0, 'Value': 0}

            data, validated = self.validation_of_parameters(data)
        
            if validated:
                last_update = timezone.now() - datetime.timedelta(minutes=30)
                currency_conversion = CurrencyConversion.objects.filter(original_currency=str(data['From']), destination_currency=str(data['To']), date__gte=last_update)
                if currency_conversion:
                    currency_conversion = currency_conversion.last()
                    data.update(Price = str(currency_conversion.value))
                else: 
                    data = self.coin_price(data)

                data = self.convert_currency(data)

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {'Internal server error'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def coin_price(self, data, **kwargs):
        try:
            response = requests.get('https://min-api.cryptocompare.com/data/price?fsym='+str(data['From'])+'&tsyms='+str(data['To']))
            cotacao = response.json()
            value = self.value_format(cotacao[data['To']])
            data.update(Price = str(value))
            currency_conversion = CurrencyConversion()
            currency_conversion.original_currency = str(data['From'])
            currency_conversion.destination_currency = str(data['To'])
            if value < 1:
                currency_conversion.lower_value = value
            else:
                currency_conversion.higher_value = value
            currency_conversion.date = timezone.now()
            currency_conversion.save()
        except:
            data.update(Price = "API cryptocompare error")
        return data
        

    def value_format(self, original_value):
        if Decimal(original_value) >=1:
            return round(original_value, 4)
        elif str(original_value).find('+') > -1:
            return Decimal('{:.1f}'.format(original_value))
        else:
            exponent = str(original_value).find('e')
            if exponent == -1:
                return Decimal(original_value)
            else:   
                shift = exponent
                if str(original_value).find('.') > -1:
                    shift -= 1
                decimal_point = -int(str(original_value)[str(original_value).find('-'):]) - 1 + shift
                floatformat = '{:.'+str(decimal_point)+'f}'
        return Decimal(floatformat.format(original_value))

    def convert_currency(self, data, **kwargs):
        value = Decimal(data['Amount']) * Decimal(data['Price'])
        data.update(Value = str(value))
        return data

    def validation_of_parameters(self, data, **kwargs):
        codes = ['USD', 'BRL', 'EUR', 'BTC', 'ETH']
        valid = True
        if data['From'] not in codes:
            data.update(From = "The currency of non-informed origin.")
            valid = False
        if data['To'] not in codes:
            data.update(To = "The currency of destination not informed.")
            valid = False
        if data['Amount'] == False or not self.is_a_number(data['Amount']) :
            data.update(Amount = "Not set value.")
            valid = False
        else:
            data.update(Amount = data['Amount'])
        return data, valid

    def is_a_number(self, value):
        try:
            float(value)
        except ValueError:
            return False
        return True