from django.db import models

class CurrencyConversion(models.Model):
    code_choices = ((u'USD', u'Dólar Americano'),
                      (u'BRL', u'Real'),
                      (u'EUR', u'Euro'),
                      (u'BTC', u'Bitcoin'),
                      (u'ETH', u'Ethereum'),)
    from_currency = models.CharField(max_length=3, choices=code_choices)
    lower_value = models.DecimalField(max_digits=10, decimal_places=8, default=0.00)
    higher_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField()
    to_currency = models.CharField(max_length=3, choices=code_choices)

    @property
    def value(self):
        if self.higher_value > 1:
            return self.higher_value
        elif self.lower_value < 1:
            return self.lower_value