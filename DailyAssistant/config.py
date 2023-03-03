import json
from json.decoder import JSONDecodeError

try:
    f = open('config.ini', 'r')
    d = json.loads(f.read())
    f.close()
    TOKEN = d["TOKEN"]
    REDIS_ENDPOINT = d["REDIS_ENDPOINT"]
    REDIS_HOST = d["REDIS_HOST"]
    REDIS_PORT = d["REDIS_PORT"]
    REDIS_PSW = d["REDIS_PSW"]
except (FileNotFoundError, JSONDecodeError) as e:
    TOKEN = input('Enter your telegram bot token: ')
    REDIS_ENDPOINT = input('Enter your redis endpoint: ')
    REDIS_HOST = input('Enter your redis host: ')
    REDIS_PORT = input('Enter your redis port: ')
    REDIS_PSW = input('Enter your redis password: ')

BASE, QUOTE, KEY, AMOUNT, CUR_RATE, APILAYER = "#BASE#", "#QUOTE#", "#KEY#", "#AMOUNT#", 'currate', 'apilayer'
SOURCE_APIS = {
    CUR_RATE: {'key': '22ff640040da2fefdb9bef89ef15a016',
               'site': 'https://currate.ru/',
               'pattern': f'https://currate.ru/api/?get=rates&pairs={BASE}{QUOTE}&key={KEY}'
               },
    APILAYER: {'key': 'bsxBIwg7amd2Tp4MwOwcKyxlpU48awDB',
               'site': 'https://apilayer.com/',
               'pattern': f'https://api.apilayer.com/currency_data/convert?to={QUOTE}&from={BASE}&amount={AMOUNT}'
               }
}
CURRENT_API = CUR_RATE

CURRENCY_CODES_URL = 'https://www.iban.com/currency-codes'
CUR_TABLE_TAG = 'tbody'

DEFAULT_CUR_DICT = {
    'РУБЛЬ': 'RUB', 'РОССИЙСКИЙ РУБЛЬ': 'RUB', 'РУБ': 'RUB', 'RUB': 'RUB',
    'ДОЛЛАР': 'USD', 'ДОЛЛАР США': 'USD', 'ДОЛ': 'USD', 'USD': 'USD',
    'ЕВРО': 'EUR', 'ЕВР': 'EUR', 'EUR': 'EUR',
    'ДРАХМ': 'AMD', 'ДРАМ': 'AMD', 'AMD': 'AMD'
}

HELP_TEXT_HEADER = '''
I can help you translate texts between languages and make currency conversion.

You can control me by sending these commands:

/start - to get my hello and this information once again:)

/help - to get this information once again 

/tr - to switch translation mode on

/cn - to switch conversion mode on

/lang - to get reference information about languages (short designations list)

'''

HELP_TEXT_TRANSLATION = '''
TRANSLATION MODE:

Just send me the text to translate. 
If it's in english, i'll automatically translate it into russian. 
Also If it's in russian, i'll automatically translate it into english.

To translate text into other languages use the following pattern:

:<lng> <text> 

for example, to translate into armenian, write :hy Hello World!

If you are not in /tr mode, you can use quick command to translate text immediately:

/tr <lng> <text> or /tr <text>

'''

HELP_TEXT_CONVERSION = '''
CONVERSION MODE:

Use the following pattern: 
<base> <quote> <amount> 
to convert amount from base currency into quote currency.

for example:
  RUB EUR 100
  доллар евро 1000
  amd рубль 500

If you are not in /cn mode, you can use quick command to make conversion immediately:
/cn <base> <quote> <amount>

All currency codes are represented below:
  
'''

HELP_TEXT = HELP_TEXT_HEADER + HELP_TEXT_TRANSLATION + HELP_TEXT_CONVERSION


