import requests
from bs4 import BeautifulSoup

from config import *


def is_float(val):
    """checks if val is floated"""
    try:
        float(str(val).replace(',', '.'))
        res = True
    except ValueError:
        res = False
    return res


class ConvertError(Exception):
    """class for catching exceptions that occur in conversion process"""
    pass


class CurrencyConverter:
    """class for currency conversions using api defined in config.py"""
    def __init__(self):
        self.cur_dict = {}

    def is_currency(self, val):
        """checks if the val is currency"""
        up = str.upper
        if val == '':
            res = False
        elif up(val) in map(up, DEFAULT_CUR_DICT.keys()):
            res = True
        else:
            res = up(val) in map(up, self.cur_dict.keys())
        return res

    def currencies_are_equal(self, base, quote):
        """checks if the base currency is equal to quote"""
        up = str.upper
        res = False
        try:
            res = DEFAULT_CUR_DICT[up(base)][2] == DEFAULT_CUR_DICT[up(quote)][2]
            is_found = True
        except KeyError:
            is_found = False

        if is_found:
            return res

        try:
            res = self.cur_dict[up(base)][2] == self.cur_dict[up(quote)][2]
            is_found = True
        except KeyError:
            is_found = False

        if is_found:
            return res
        else:
            raise ConvertError(f'One of comparing currencies{base, quote} is incorrect')

    def get_mnemo_code(self, currency):
        """gets mnemo code of currency"""
        up = str.upper
        try:
            result = DEFAULT_CUR_DICT[up(currency)]
        except KeyError:
            result = None
        if not result:
            try:
                result = self.cur_dict[up(currency)]
            except KeyError:
                result = None
        return result

    def load_currency_dict(self):
        """loads the reference information from internet (source site is defined in config.py)"""
        html = requests.get(CURRENCY_CODES_URL).content
        cur = BeautifulSoup(html, 'html.parser').find(CUR_TABLE_TAG)
        cur = cur.findChild('tr') if cur else None
        if cur:
            while cur:
                country = cur.findChild('td')
                cur_name = country.findNext('td')
                cur_mnemo = cur_name.findNext('td')
                cur_iso = cur_mnemo.findNext('td')
                # print(country.text, cur_name.text, cur_MNEMO.text, cur_ISO.text)
                self.cur_dict[str.upper(cur_name.text)] = (country.text, cur_name.text, cur_mnemo.text, cur_iso.text)
                self.cur_dict[cur_mnemo.text] = (country.text, cur_name.text, cur_mnemo.text, cur_iso.text)
                cur = cur.findNext('tr')
        else:
            self.cur_dict = DEFAULT_CUR_DICT

    def convert(self, base, quote, amount):
        """converts amount from base to quote currency"""
        if not self.is_currency(base):
            raise ConvertError('value of base currency is incorrect')
        if not self.is_currency(quote):
            raise ConvertError('value of quote currency is incorrect')
        if not is_float(amount):
            raise ValueError('value of amount to convert should be numeric')
        if self.currencies_are_equal(base, quote):
            raise ConvertError('currencies are equal')

        base = self.get_mnemo_code(base)
        quote = self.get_mnemo_code(quote)

        key = SOURCE_APIS[CURRENT_API]['key']
        req = str(SOURCE_APIS[CURRENT_API]['pattern']).replace(KEY, key)
        req = req.replace(BASE, base).replace(QUOTE, quote)

        if CURRENT_API == CUR_RATE:
            res = requests.get(req)
            res = json.loads(res.content)
            res = res['data'][base + quote]
            res = float(res) * float(amount)
        elif CURRENT_API == APILAYER:
            req = req.replace(AMOUNT, str(amount))

            payload = {}
            headers = {"apikey": key}

            res = requests.request("GET", req, headers=headers, data=payload)
            res = json.loads(res.content)
            res = res['result']
        else:
            raise ConvertError('No conversion API source specified')
        return res


conv = CurrencyConverter()
conv.load_currency_dict()

if __name__ == '__main__':
    print(conv.convert('USD', 'RUB', 100))
    # print(conv.currencies_are_equal('RUB', 'EUR'))
