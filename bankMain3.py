from abc import ABC, abstractmethod, abstractclassmethod

AGENCY_NUMBER = "0001"
WITHDRAWAL_LIMIT = 500
WITHDRAWAL_LIMIT_PER_DAY = 3

class Transaction(ABC):
    @property
    @abstractmethod
    def amount(self):
        pass

    @abstractclassmethod
    def register(self, Account):
        pass

class Deposit(Transaction):
    def __init__(self, Amount):
        self.Amount = Amount

    @property
    def amount(self):
        return self.Amount
    
    def register(self, Account):
        resultTransaction = Account.deposit(self.amount)

        if resultTransaction:
            Account.history.addTransaction(self)
            return True
        return False

class Withdraw(Transaction):
    def __init__(self, Amount):
        self.Amount = Amount

    @property
    def amount(self):
        return self.Amount
    
    def register(self, Account):
        resultTransaction = Account.withdraw(self.amount)

        if resultTransaction:
            Account.history.addTransaction(self)
            return True
        return False

class History():
    def __init__(self):
        self.transactions = []

    @property
    def allTransactions(self):
        return self.transactions

    def addTransaction(self, transaction):
        self.transactions.append([
            transaction.__class__.__name__,
            transaction.Amount
        ])

class Client():
    def __init__(self, neighborhood, accounts):
        self.neighborhood = neighborhood
        self.accounts = []

    def carryOutTransaction(self, Account, Transaction):
        Account.history.addTransaction(Transaction)
    def addAccount(self, Account):
        self.accounts.append(Account)

class PhysicalPersona(Client):
    def __init__(self, cpf, name, birthDay, neighborhood=None, accounts=None):
        super().__init__(neighborhood, accounts)
        self.__cpf = cpf
        self.__name = name
        self.__birthDay = birthDay

class Account():
    def __init__(self, account_number, Client):
        self.__balance = 0
        self.__account_number = account_number
        self.__agency = AGENCY_NUMBER
        self.__client = Client
        self.__history = History()

    @classmethod
    def newAccount(cls, Client, account_number):
        return cls(account_number, Client)
    
    @property
    def balance(self):
        return self.__balance

    @property
    def account_number(self):
        return self.__account_number

    @property
    def agency(self):
        return self.__agency

    @property
    def client(self):
        return self.__client

    @property
    def history(self):
        return self.__history

        
    def withdraw(self, amount):
        balance = self.__balance

        if amount > balance:
            print(f"Saldo insuficiente.")
        elif amount > 0:
            self.__balance -= amount
            print(f"Saque de R$ {amount:.2f} realizado com sucesso!")
            return True
        else:
            print(f"Valor de saque inválido.")
        return False

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Depósito de R$ {amount:.2f} realizado com sucesso!")
            return True
        else:
            print(f"Valor de depósito inválido.")
        return False

class checkingAccount(Account):
    def __init__(self, account_number, Client, limit=WITHDRAWAL_LIMIT_PER_DAY, withdrawal_limit=WITHDRAWAL_LIMIT):
        super().__init__(account_number, Client)
        self.__limit = limit
        self.__withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        withdrawls_limits = len([transaction for transaction in self.history.transactions if isinstance(transaction, Withdraw)])

        if withdrawls_limits >= self.__limit:
            print(f"Limite de saques diários atingido.")
        elif amount > self.__withdrawal_limit:
            print(f"Limite de saque excedido.")
        else:
            return super().withdraw(amount)
        return False
    
    def __str__(self):
        return f"Conta Corrente - Número: {self.account_number}, Agência: {self.agency}, Saldo: R$ {self.balance:.2f}"
        