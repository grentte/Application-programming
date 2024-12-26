import telebot
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Это бот с интересными фактами. Введите одну из функций:\n"
                 "- /random - Случайный факт\n"
                 "- /theme - Факт на выбранную тему\n"
                 "- /settheme - Выбрать любимую тему\n"
                 "- /gettheme - Получить факт по любимой теме")



bot.infinity_polling()
