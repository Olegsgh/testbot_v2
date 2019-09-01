import argparse
import os
import telebot
import reply_bot

from flask import Flask, request

API_TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(API_TOKEN)

server = Flask(__name__)
TELEBOT_URL = 'telebot_webhook/'
BASE_URL = 'https://testbot-heroku-v2.herokuapp.com/'

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    response = reply_bot.reply_with_log(message, message.text)
    bot.reply_to(message, response)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    response = reply_bot.reply_with_log(message, "Привет, можешь подписаться на новости, либо получить отчет.")
    bot.reply_to(message, response)

@bot.message_handler(regexp="Отчёт \d{4}-\d{2}-\d{2}")
def send_welcome(message):
    response = reply_bot.reply_full_week_report(message)
    bot.reply_to(message, response)

@bot.message_handler(regexp="Отчёт \d{4}-\d{2}-\d{2} сумма")
def send_welcome(message):
    response = reply_bot.reply_kredit_week_report(message)
    bot.reply_to(message, response)

@bot.message_handler(regexp="Отчёт \d{4}-\d{2}-\d{2} сумма количество")
def send_welcome(message):
    response = reply_bot.reply_full_week_report(message)
    bot.reply_to(message, response)

@bot.message_handler(regexp="Отчёт \d{4}-\d{2}-\d{2} количество")
def send_welcome(message):
    response = reply_bot.reply_count_week_report(message)
    bot.reply_to(message, response)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    reply_bot.reply_with_log(message, message.text)

@server.route('/' + TELEBOT_URL + API_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=BASE_URL + TELEBOT_URL + API_TOKEN)
    return "!", 200

@server.route("/show_logs")
def show_logs():
    return reply_bot.get_old_message(), 200

parser = argparse.ArgumentParser(description='Run the bot')
parser.add_argument('--poll', action='store_true')
args = parser.parse_args()

if args.poll:
    bot.remove_webhook()
    bot.polling()
else:
    # webhook should be set first
    webhook()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))





