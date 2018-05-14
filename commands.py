# прописаны команды для хендлеров

import weather
import os
import db
from telegram import KeyboardButton, ReplyKeyboardMarkup

# приветствие от бота
def start_command(bot, update):
    welcome = 'Hello!\n' \
              'Type /help to find out how bot works.'
    bot.send_message(chat_id=update.message.chat_id, text=welcome)


# описание доступных команд
def help_command(bot, update):
    response = 'Type a name of the city to watch weather forecast\n' \
               'Note: \n' \
               'You can add "ru" or other 2-letter name of the country ' \
               'after comma to the end of request.\n' \
               'If you want to save your home location, ' \
               'type \'/set name of city\'\n' \
               'To get a forecast for your home location type \'/home\''
    bot.send_message(chat_id=update.message.chat_id, text=response)


# дейстивя на сообщение от юзера
# если город, то выдаем прогноз погоды (функции в weather)
# если выбранна кнопка смены дом. локации, то выводим инструкцию для ее смены
# иначе - некорректный ввод
def text_messg_command(bot, update):
    city = update.message.text
    if city == 'Change home location':
        bot.send_message(chat_id=update.message.chat_id,
                         text='Type new home location in format \'/set City\'')
        return
    try:
        response, status = weather.info(city)
    except BaseException:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Incorrect city. Please, try again.\n\n')
        return
    bot.send_message(chat_id=update.message.chat_id, text=response)
    bot.send_photo(chat_id=update.message.chat_id,
                   photo=open('images/graph' + city + '.png', 'rb'))
    os.remove('images/graph' + city + '.png')


# достаем сохраненную домашнюю локации
# храним ее в базе данных (подключаем из db)
def get_home_city(bot, update):
    list_cities = db.get_cities(update.message.chat_id)
    # если в базе еще нет сохраненной локации, то сообщаем об этом юзеру
    if len(list_cities) == 0:
        bot.send_message(chat_id=update.message.chat_id,
                         text='You haven\'t add your home location yet')
    # создаем кнопки с выбором город/изменить город
    else:
        home = list_cities[0]
        button = [[KeyboardButton(home)],
                  [KeyboardButton('Change home location')]]
        button_markup = ReplyKeyboardMarkup(button,
                                            one_time_keyboard=True,
                                            resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Your home location is ' + home,
                         reply_markup=button_markup)


# для смены домашней локации
# удаляем из базы старый город, добавляем новый
def set_home_location(bot, update):
    city = update.message.text.split()[-1]
    try:
        response, status = weather.info(city)
    except BaseException:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Incorrect request. Please, try again.\n\n')
        return
    db.remove_all_for_user(update.message.chat_id)
    db.add(update.message.chat_id, city)
    reply_text = 'Now ' + city + ' is your new home location!'
    bot.send_message(chat_id=update.message.chat_id, text=reply_text)
