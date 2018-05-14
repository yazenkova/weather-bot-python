# прописаны основные хендлеры
# команды для них лежат в commands
# API, токен для бота и прокси лежат в config
# наши команды: /start, /help,
# /set - запоминает домашнюю локацию 
# /home - предлагает узнать прогноз в домашней локации

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config
import commands

updater = Updater(token=config.token, request_kwargs=config.proxy)
dispatcher = updater.dispatcher

start_command_handler = CommandHandler('start', commands.start_command)
text_messg_handler = MessageHandler(Filters.text, commands.text_messg_command)
help_command_handler = CommandHandler('help', commands.help_command)
get_home_command_handler = CommandHandler('home', commands.get_home_city)
set_home_command_handler = CommandHandler('set', commands.set_home_location)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_messg_handler)
dispatcher.add_handler(help_command_handler)
dispatcher.add_handler(get_home_command_handler)
dispatcher.add_handler(set_home_command_handler)

updater.start_polling(clean=True)
updater.idle()
