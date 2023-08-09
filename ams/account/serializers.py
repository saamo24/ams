from rest_framework import serializers
from .models import Account
from user.models import User

class AccountBalanceSerializer(serializers.Serializer):
    currency = serializers.CharField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    def get_account_balances(self, user):
        accounts = Account.objects.filter(owner=user)
        balances = []
        for account in accounts:
            balances.append({
                'currency': account.currency,
                'balance': account.amount
            })
        return balances

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['currency', 'amount','owner']

    def validate(self, data):
        owner = data['owner']
        currency = data['currency']

        existing_accounts = Account.objects.filter(owner=owner, currency=currency)
        if existing_accounts.exists():
            raise serializers.ValidationError("User already has an account with this currency.")

        return data

    def create(self, validated_data):
        
        account = Account.objects.create(**validated_data)
        account.save()
        return account
        
class DepositSerializer(serializers.Serializer):
    amount = serializers.FloatField()

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Deposit amount must be greater than 0.")
        return value

class WithdrawSerializer(serializers.Serializer):
    amount = serializers.FloatField()

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Withdrawal amount must be greater than 0.")
        return value

class TransactionSerializer(serializers.Serializer):

    transaction_type = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateTimeField()
