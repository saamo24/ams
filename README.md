# AMS

## Task: Account Management System
### Introduction:
The Account Management System with Registration, Login, Currency Accounts, and Balance Calculation is a software project designed to provide users with a secure platform to register, log in, create currency accounts in various denominations, perform transactions, and calculate balances for each account. This system enables individuals to manage their funds efficiently and keep track of their account balances in real-time.

1. User Registration and Login:
 - `/register` Allow users to register by providing necessary information such as name, email address, and password.
 - `/login` Implement a robust authentication system to verify user credentials during the login process.
2. Open New Currency Accounts:
 - `/username/open` Enable registered users to open new currency accounts using available currencies, such as USD, AMD, RUB, and more.
 - User should have only one account for a currency
 - Assign unique account numbers or identifiers to each newly created currency account.
3. Account Management:
 - `/username/balance` Allow users to view their account balances for each currency account in real-time.
 - `/username/deposit/<account-number>` Enable users to deposit funds into their currency accounts by specifying the desired currency and amount.
 - `/username/withdraw/<account-number>` Implement withdrawal functionality, allowing users to request withdrawals from their currency accounts. Perform necessary validations to ensure sufficient account balance for withdrawals.
4. Transaction History and Statements:
 - `/username/transactions/<account-number>` Maintain a comprehensive transaction history for each currency account, including deposits, withdrawals, and currency conversions.
 - `/username/statements/<account-number>` Enable users to view and download account statements summarizing their transactions over a specific period.
