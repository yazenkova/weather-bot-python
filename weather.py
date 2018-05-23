# работа с данными с сайта openweathermap.org
# для удобства подключена библиотека pyowm
# для построения графиков пользуемся matplotlib
import os
import pyowm
import config
import matplotlib.pyplot as plt
from collections import OrderedDict


def short_information(weather):
    weather_dict = OrderedDict()
    if weather.get_temperature(unit='celsius')['temp'] > 0:
        weather_dict['Temperature:'] = '+' + str(weather.get_temperature(unit='celsius')['temp'])
    else:
        weather_dict['Temperature:'] =str(weather.get_temperature(unit='celsius')['temp'])
    weather_dict['Status:'] = str(weather.get_detailed_status())
    weather_dict['Humidity:'] = str(weather.get_humidity()) + '%'
    weather_dict['Pressure:'] = str(int(weather.get_pressure()['press'] / 1.3332239)) + ' mmhg'
    weather_dict['Wind:'] = str(weather.get_wind()['speed']) + ' m/s'
    return weather_dict


# построение графика по данным о температуре на ближайшие 5 дней
# сохраняем его как файл .png (после отправки сразу же удаляем)
def make_image(forecast, city):
    if not os.path.exists('images'):
        os.makedirs('images')
    x_data = []
    y_data = []
    for weather in forecast:
        dt = str(weather.get_reference_time(timeformat='iso'))
        x_data.append(dt[8:10] + '.' + dt[5:7] + '\n' + dt[10:13] + ':00')
        y_data.append(int(weather.get_temperature(unit='celsius')['temp']))
    fig = plt.figure(figsize=(30, 15))
    plt.style.use('seaborn-whitegrid')
    ax = plt.axes()
    plt.plot(x_data, y_data)
    ax.set_title('Forecast in ' + city + ' for 5 days', size=25)
    ax.set_xlabel('date/time', size=20)
    ax.set_ylabel('temperature in Celsius', size=20)
    plt.savefig('images/graph' + city + '.png', format='png')


def information(city):
    owm = pyowm.OWM(API_key=config.api_key, language='en')
    forecast = owm.three_hours_forecast(city)
    f = forecast.get_forecast()
    w = f.get_weathers()[0]
    info = short_information(w)
    response = 'City: ' + city + '\n'
    for key in info.keys():
        response += key + ' ' + info[key] + '\n'
    make_image(f, city)
    return response
