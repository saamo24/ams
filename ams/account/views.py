from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AccountSerializer, AccountBalanceSerializer, DepositSerializer, WithdrawSerializer, TransactionSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.models import User
from .models import Account
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
import json
from django.http import HttpResponse
from rest_framework import status
import csv

# Create your views here.

class WalletView(APIView):
    
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        data = request.data.copy()
        owner = User.objects.get(username=kwargs['username'])
        data.update({'owner': owner.id})
        serializer = AccountSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
   
class AccountBalanceView(APIView):
    def get(self, request, username):
        try:
            owner = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found."})
        
        serializer = AccountBalanceSerializer()
        balances = serializer.get_account_balances(owner)
        
        return Response(balances, status=HTTP_200_OK)

class AccountDepositView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, username, account_number):
        user = get_object_or_404(User, username=username)
        account = get_object_or_404(Account, owner=user, account_number=account_number)

        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']

            account.amount += amount
            account.save()

            transaction_data = {
            "transaction_type": "deposit",
            "amount": amount,
            "date": datetime.now().isoformat()
            }   
            account.transaction_history.append(transaction_data)
            account.save()

            return Response({"message": f"Successfully deposited {amount} into your account."}, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_404_NOT_FOUND)
 
class WithdrawView(APIView):
    
    permission_classes = [IsAuthenticated]

    def put(self, request, username, account_number):
        user = get_object_or_404(User, username=username)
        account = get_object_or_404(Account, owner=user, account_number=account_number)

        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']

            account.amount -= amount
            account.save()

            transaction_data = {
            "transaction_type": "withdrawal",
            "amount": amount,
            "date": datetime.now().isoformat()
            }
            account.transaction_history.append(transaction_data)
            account.save()

            return Response({"message": f"Successfully withdrawed {amount} from your account."}, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_404_NOT_FOUND)

class TransactionHistoryView(APIView):
    def get(self, request, username, account_number):
        user = get_object_or_404(User, username=username)
        account = get_object_or_404(Account, owner=user, account_number=account_number)

        transaction_history = account.transaction_history
        serializer = TransactionSerializer(transaction_history, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

class AccountStatementView(APIView):
    def get(self, request, username, account_number):
        try:
            user = User.objects.get(username=username)
            account = Account.objects.get(owner=user, account_number=account_number)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({"error": f"No account found with account number: {account_number}"}, status=HTTP_404_NOT_FOUND)

        transactions_history = account.transaction_history

        json_data = json.dumps(transactions_history, indent=4)

        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{username}_transaction_history.json"'

        # TODO download .csv files NOT json
        

        return response

        return Response(transactions_history, status=HTTP_200_OK)
