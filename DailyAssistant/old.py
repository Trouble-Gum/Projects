import telebot
# import socket
import googletrans
# import playsound
# from google_trans_new import google_translator
#
# from googletrans import Translator
# from gtts import gTTS
# import os

# hostname = socket.gethostname()
translator = google_translator()
# speak = gTTS(text="շնորհակալություն", lang='hy', slow=False)
# speak.save("C:\SDATA\captured_voice.mp3")

# Using OS module to run the translated voice.
# playsound.playsound("C:\captured_voice.mp3")
# os.remove('captured_voice.mp3')

# creating an instance of the class
bot = telebot.TeleBot('5769485841:AAGFZd21dqqLQ0uyAiPHUi5M1ckuczmuoPQ')


# print(googletrans.LANGUAGES)
# exit()

# Function that handle the command /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, "Hi! I'm in touch. Write me smth :)")


# Receiving the user messages
@bot.message_handler(content_types=["text"])
def handle_text(message):
    chat = bot.get_chat(message.chat.id)
    username = chat.first_name
    if username is None:
        username = chat.username
    res = "!!!"
    # res = translator.translate(message.text, lang_tgt='hy', pronounce=True)
    # f = open('C:/SDATA/txt.txt', 'a')
    # f.write(message.text + "\n")
    # f.close()
    bot.send_message(message.chat.id, res)  # f"Dear {username}, the translation of your message is following: {res}" )
    # bot.send

# Bot Startup
bot.polling(none_stop=True, interval=0)
