import telebot
from telebot import types
import os

bot = telebot.TeleBot('7095549792:AAFqExmSpSVjBUmjZOLswciPuE7YZbwpG-U')

@bot.message_handler(commands=['start','help'])

