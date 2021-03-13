import requests
import json


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


class NotSuchCurrencyException(Exception):
    def __init__(self, currency):
        self.currency = currency

    def __str__(self):
        return f'Неверная запись валюты: {self.currency}'


class WrongAmount(Exception):
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return f'Ожидалось положительное число, а было {self.amount}'


def validation(func):
    def wrapper(base, quote, amount):
        if base not in Currency.get_names():
            raise NotSuchCurrencyException(base)

        if quote not in Currency.get_names():
            raise NotSuchCurrencyException(quote)

        if not is_digit(amount) or float(amount) < 0:
            raise WrongAmount(amount)

        return func(base, quote, amount)

    return wrapper


class Conversion:
    @staticmethod
    @validation
    def get_price(base, quote, amount):
        data = json.loads(requests.get(f'https://api.exchangeratesapi.io/'
                                       f'latest?base={base}&symbols={quote}')
                          .content)
        factor = float(data['rates'][quote])
        amount = float(amount)
        return amount * factor


def decorator(f):
    def wrapper(base="USD", values=None):
        if base and base not in Currency.get_names():
            raise NotSuchCurrencyException(base)
        if values and values not in Currency.get_names():
            raise NotSuchCurrencyException(values)
        return f(base, values)

    return wrapper


class Currency:
    currencies = list()

    @staticmethod
    def get_names():
        if not Currency.currencies:
            Currency.currencies = list(Currency.get().keys())
            Currency.currencies.sort()

        return Currency.currencies

    @staticmethod
    def get(base="USD", values=None):
        if values:
            data = json.loads(requests.get(f'https://api.exchangeratesapi'
                                           f'.io/latest?base='
                                           f'{base}&symbols={values}').content)
        else:
            data = json.loads(requests.get(f'https://api.exchangeratesapi'
                                           f'.io/latest?base='
                                           f'{base}').content)

        return data['rates']

    @staticmethod
    @decorator
    def get_sorted(base="USD", values=None):
        currencies = Currency.get(base, values)
        sorted_currencies = dict()
        for key in Currency.get_names():
            sorted_currencies[key] = currencies[key]
        return sorted_currencies


# print(Conversion.get_price("RUB", "USD", "30000"))
# print(Currency.get_sorted('RUB'))
