import telebot
import requests
from bs4 import BeautifulSoup
import random

from config import BOT_TOKEN, SITE_URL

bot = telebot.TeleBot(BOT_TOKEN)

# Функция для получения HTML и парсинга страницы
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return None


# Функция для извлечения случайного факта
def get_random_fact():
    page_number = random.randint(1, 4330)  # Генерируем случайный номер страницы
    url = f"{SITE_URL}/from{page_number}"
    soup = fetch_html(url)

    if soup:
        facts = soup.find_all('p', class_='content')
        clean_facts = [c.text for c in facts]
        if clean_facts:
            fact = random.choice(facts)
            return fact
    return "Не удалось получить случайный факт. Попробуйте позже."


# Функция для извлечения факта по теме
def get_fact_by_topic(topic):
    url = f"{SITE_URL}/{topic}"
    soup = fetch_html(url)

    if soup:
        facts = soup.find_all('p', class_='content')
        clean_facts = [c.text for c in facts]
        if clean_facts:
            fact = random.choice(facts)
            return fact
    return f"Не удалось найти факты на тему: {topic}. Попробуйте позже."


# Обработчики команд
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может прислать интересные факты. Вот что я умею:\n\n"
                                      "/random - случайный факт\n"
                                      "/sport - факт о спорте\n"
                                      "/music - факт о музыке\n"
                                      "/nature - факт о природе", parse_mode='HTML')


@bot.message_handler(commands=['random'])
def send_random_fact(message):
    fact = get_random_fact()
    bot.send_message(message.chat.id, fact, parse_mode='HTML')


@bot.message_handler(commands=['sport'])
def send_sport_fact(message):
    fact = get_fact_by_topic('sport')
    bot.send_message(message.chat.id, fact, parse_mode='HTML')


@bot.message_handler(commands=['music'])
def send_music_fact(message):
    fact = get_fact_by_topic('music')
    bot.send_message(message.chat.id, fact, parse_mode='HTML')


@bot.message_handler(commands=['nature'])
def send_nature_fact(message):
    fact = get_fact_by_topic('nature')
    bot.send_message(message.chat.id, fact, parse_mode='HTML')


# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
