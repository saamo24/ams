from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from user.models import User

# Create your models here.

class CurrencyTypes(models.Choices):
    AMD = 'AMD'
    USD = 'USD'
    RUB = 'RUB'
    EUR = 'EUR'
    BTC = 'BTC'

class Account(models.Model):

    class Meta:
        db_table = 'account'
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    account_number = models.UUIDField(unique=True, default=uuid4)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='accounts')
    currency = models.CharField(max_length=3, choices=CurrencyTypes.choices)
    amount = models.FloatField(default=0.0, blank=True, null=True)
    transaction_history = models.JSONField(default=list)
