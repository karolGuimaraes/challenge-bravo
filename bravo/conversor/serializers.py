from rest_framework import serializers
from conversor.models import CurrencyConversion
#serializer = CurrencyConversionSerializer(currency_conversion, context=data)

class CurrencyConversionSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_amount(self, obj):
        return self.context.get("amount")
    
    def get_price(self, obj):
        return self.context.get("price")

    def get_value(self, obj):
        return self.context.get("value")

    class Meta:
        model = CurrencyConversion
        fields = ('amount', 'price', 'value')
        # read_only_fields = ('from_currency', 'to_currency')

