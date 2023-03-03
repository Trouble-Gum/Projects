import config as cf
import redissynchronizer
import telebot

from currencyconverter import conv, ConvertError
from redissynchronizer import rs
from extensions import *

# creating an instance of the class
bot = telebot.TeleBot(cf.TOKEN)
log('Telegram bot DailyAssistant has been created', INFO)

up = str.upper  # just override method with shorter name


# function that handle commands
@bot.message_handler(commands=["start", "cn", "tr", "help", "lang"])
def start(m):
    params = str(m.text).split()
    chat = bot.get_chat(m.chat.id)
    command = params[0][1:]
    username = chat.first_name
    if username is None:
        username = chat.username
    if up(command) == 'START':
        log(f'{chat.username} has started using bot', INFO)  # log the action
        bot.send_message(m.chat.id,
                         f"Hi, {username}! I'm in touch with you! \n" +
                         cf.HELP_TEXT_HEADER
                         )

        img = open('./images/Translation.jpg', 'rb')
        bot.send_photo(m.chat.id, photo=img)
        bot.send_message(m.chat.id, cf.HELP_TEXT_TRANSLATION)

        img = open('./images/Conversion.jpg', 'rb')
        bot.send_photo(m.chat.id, photo=img)
        bot.send_message(m.chat.id,
                         cf.HELP_TEXT_CONVERSION +
                         cf.CURRENCY_CODES_URL
                         )

    if up(command) == 'HELP':
        bot.send_message(m.chat.id,
                         cf.HELP_TEXT +
                         cf.CURRENCY_CODES_URL
                         )
    if up(command) == 'LANG':
        bot.send_message(m.chat.id, str(LANGUAGES))

    rs.put_user_mode_into_cache(chat.username, up(command))  # do not unload user settings immediately
    # use postponed and batched mode (see RedisSynchronizer class definition)

    if len(params) > 1:  # case when command was entered with params (quick command)
        m.text = ' '.join(params[1:])
        handle_text(m, command)


# receive the user messages
@bot.message_handler(content_types=["text"])
def handle_text(message, mode=None):
    if mode and up(mode) in ('START', 'HELP', 'LANG'):  # command reminder/suggestion
        res = 'To work with this bot use commands:\n' \
              '/tr /cn /lang \n' \
              'To get help write /help'
        bot.send_message(message.chat.id, res)
    elif mode and up(mode) == 'CN':  # conversion mode
        res, base, quote, amount = None, None, None, None
        try:
            base, quote, amount = str(message.text).split()
        except ValueError:
            res = 'invalid number of input params'
        try:
            res = conv.convert(base, quote, amount) if not res else res
        except (ConvertError, ValueError) as e:
            res = e
        bot.send_message(message.chat.id, res)
    elif mode and up(mode) == 'TR':  # translation mode
        res = translate(message.text)
        bot.send_message(message.chat.id, res, )
    else:  # if the input parameter mode was not passed
        cur_mode = rs.get_actual_user_mode(message.chat.username)  # try to get mode from cache
        if cur_mode:
            handle_text(message, mode=cur_mode)
        else:
            bot.send_message(message.chat.id, 'Please, send command /start to start interaction with this bot. ')


with CleanExit(redissynchronizer.force_synchronize):  # context manager for correct ending,
    # for example keyboard interruption
    try:  # events polling loop
        bot.polling(none_stop=True, interval=0)
    except Exception as ex:
        log(ex, ERROR)  # log the error
        redissynchronizer.force_synchronize()
