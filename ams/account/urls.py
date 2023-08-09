from django.urls import path
from .views import (WalletView,
                    AccountBalanceView,
                    AccountDepositView,
                    WithdrawView,
                    TransactionHistoryView,
                    AccountStatementView
                )

urlpatterns = [
    path('<slug:username>/open/', WalletView.as_view(), name='open'),
    path('<slug:username>/balance/', AccountBalanceView.as_view(), name='balance'),
    path('<slug:username>/deposit/<slug:account_number>', AccountDepositView.as_view(), name='deposit'),
    path('<slug:username>/withdraw/<slug:account_number>', WithdrawView.as_view(), name='withdraw'),
    path('<slug:username>/transaction/<slug:account_number>', TransactionHistoryView.as_view(), name='transaction'),
    path('<slug:username>/statements/<slug:account_number>', AccountStatementView.as_view(), name='statments'),
]