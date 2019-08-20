# from django.shortcuts import render
from conversor.models import CurrencyConversion
# from rest_framework.views import APIView
from rest_framework.response import Response
from conversor.serializers import CurrencyConversionSerializer
from rest_framework import status
import requests
import json
from rest_framework.throttling import UserRateThrottle
import datetime
from datetime import timedelta 
from decimal import Decimal
from django.utils import timezone

from rest_framework.renderers import JSONRenderer

from rest_framework.decorators import api_view, throttle_classes, renderer_classes


class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1500/second'


@throttle_classes([UserRateThrottle])
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def currency_conversion(request, format=None):
    from_currency = request.GET.get('from', False)
    to_currency = request.GET.get('to', False)
    amount = request.GET.get('amount', False)
    try:
        data = {'from_currency': from_currency, 'to_currency': to_currency, 'amount': amount, 'price': 0, 'value': 0}
        validated = validation_of_parameters(data)
        if validated:
            last_update = timezone.now() - datetime.timedelta(minutes=30)
            currency_conversion = CurrencyConversion.objects.filter(from_currency=str(data['from_currency']), to_currency=str(data['to_currency']), date__gte=last_update)
            if currency_conversion.exists():
                currency_conversion = currency_conversion.last()
                data.update(price = str(currency_conversion.value))
            else: 
                currency_conversion = coin_price(data)

            data.update(value = str(Decimal(data['amount']) * Decimal(data['price'])))
            #serializer = CurrencyConversionSerializer(currency_conversion, context=data)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'Internal server error :('}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def coin_price(data, **kwargs):
    currency_conversion = None
    try:
        response = requests.get('https://min-api.cryptocompare.com/data/price?fsym='+str(data['from_currency'])+'&tsyms='+str(data['to_currency']))
        cotacao = response.json()
        value = value_format(cotacao[data['to_currency']])
        data.update(price = str(value))
        currency_conversion = CurrencyConversion()
        currency_conversion.from_currency = str(data['from_currency'])
        currency_conversion.to_currency = str(data['to_currency'])
        if value < 1:
            currency_conversion.lower_value = value
        else:
            currency_conversion.higher_value = value
        currency_conversion.date = timezone.now()
        currency_conversion.save()
    except:
        data.update(price = "API cryptocompare error")
    return currency_conversion
    
def value_format(original_value):
    if Decimal(original_value) >=1:
        return round(original_value, 4)
    elif str(original_value).find('+') > -1:
        return Decimal('{:.1f}'.format(original_value))
    else:
        exponent = str(original_value).find('e')
        if exponent == -1:
            return Decimal(original_value)
        else:   
            if str(original_value).find('.') > -1:
                exponent -= 1
            decimal_point = -int(str(original_value)[str(original_value).find('-'):]) - 1 + exponent
            floatformat = '{:.'+str(decimal_point)+'f}'
    return Decimal(floatformat.format(original_value))

def validation_of_parameters(data, **kwargs):
    codes = ['USD', 'BRL', 'EUR', 'BTC', 'ETH']
    valid = True
    if data['from_currency'] not in codes:
        data.update(from_currency = "The currency of non-informed origin.")
        valid = False
    if data['to_currency'] not in codes:
        data.update(to_currency = "The currency of destination not informed.")
        valid = False
    if data['amount'] == False or not is_a_number(data['amount']) :
        data.update(amount = "Not set value.")
        valid = False
    else:
        data.update(amount = data['amount'])
    return valid

def is_a_number(value):
    try:
        float(value)
    except ValueError:
        return False
    return True