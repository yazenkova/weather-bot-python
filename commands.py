# прописаны команды для хендлеров

import weather
import os
import db
from pyowm.exceptions import OWMError
import logging

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    filemode='w', filename=u'bot_log.log',
                    level=logging.INFO)


def try_request_forecast(city, bot, update):
    try:
        response, status = weather.info(city)
    except OWMError:
        logging.error(u'Incorrect request. There is no such city')
        bot.send_message(chat_id=update.message.chat_id,
                         text='Incorrect city. Please, try again.\n\n')
        return
    bot.send_message(chat_id=update.message.chat_id, text=response)
    bot.send_photo(chat_id=update.message.chat_id,
                   photo=open('images/graph' + city + '.png', 'rb'))
    logging.info(u'Request completed')
    os.remove('images/graph' + city + '.png')


# приветствие от бота
def start_command(bot, update):
    logging.info(u'Try to call command /start')
    welcome = 'Hello!\n' \
              'Type /help to find out how bot works.'
    bot.send_message(chat_id=update.message.chat_id, text=welcome)
    logging.info(u'Request completed')


# описание доступных команд
def help_command(bot, update):
    logging.info(u'Try to call command /set')
    response = 'Type a name of the city to watch weather forecast\n' \
               'Note: \n' \
               'You can add "ru" or other 2-letter name of the country ' \
               'after comma to the end of request.\n' \
               'If you want to save your home location, ' \
               'type \'/set name of city\'\n' \
               'To get a forecast for your home location type \'/home\''
    bot.send_message(chat_id=update.message.chat_id, text=response)
    logging.info(u'Request completed')


# дейстивя на сообщение от юзера
# если город, то выдаем прогноз погоды (функции в weather)
# если выбранна кнопка смены дом. локации, то выводим инструкцию для ее смены
# иначе - некорректный ввод
def text_messg_command(bot, update):
    city = update.message.text
    logging.info(u'Try to request a forecast in "' + city + '"')
    if city == 'Change home location':
        bot.send_message(chat_id=update.message.chat_id,
                         text='Type new home location in format \'/set City\'')
        return
    try_request_forecast(city, bot, update)


# достаем сохраненную домашнюю локации
# храним ее в базе данных (подключаем из db)
def get_home_city(bot, update):
    logging.info(u'Try to request a forecast at home location')
    list_cities = db.get_cities(update.message.chat_id)
    # если в базе еще нет сохраненной локации, то сообщаем об этом юзеру
    if len(list_cities) == 0:
        bot.send_message(chat_id=update.message.chat_id,
                         text='You haven\'t added your home location yet')
        logging.warning(u'There is no set home location')
    # делаем запрос для сохраненного города
    else:
        home = list_cities[0]
        try_request_forecast(home, bot, update)


# для смены домашней локации
# удаляем из базы старый город, добавляем новый
def set_home_location(bot, update):
    text = update.message.text
    n = len(text)
    if n <= 4:
        city = ''
        logging.info(u'Try to set home location as " "')
    else:
        city = text[5:n]
        logging.info(u'Try to set home location as "' + city + '"')
    try:
        response, status = weather.info(city)
    except OWMError:
        logging.error(u'Incorrect request. There is no such city')
        bot.send_message(chat_id=update.message.chat_id,
                         text='Incorrect request. Please, try again.\n\n')
        return
    db.remove_all_for_user(update.message.chat_id)
    db.add(update.message.chat_id, city)
    reply_text = 'Now ' + city + ' is your new home location!'
    bot.send_message(chat_id=update.message.chat_id, text=reply_text)
    logging.info(u'Request completed')
