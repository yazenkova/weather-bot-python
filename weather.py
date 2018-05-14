# работа с данными с сайта openweathermap.org
# для удобства подключена библиотека pyowm
# для построения графиков пользуемся matplotlib
import pyowm
import config
import matplotlib.pyplot as plt


# сохраненние нужной информации
def get(city):
    owm = pyowm.OWM(API_key=config.api_key, language='en')
    obs = owm.weather_at_place(city)
    w = obs.get_weather()
    fc = owm.three_hours_forecast(city)
    f = fc.get_forecast()
    return w, f, obs.get_location().get_country()


# выделение нужной информации в словарь
def format_weather(weather):
    t = weather.get_temperature(unit='celsius')
    ans = dict()
    ans['Current temperature'] = t['temp']
    ans['Maximum temperature'] = t['temp_max']
    ans['Minimum temperature'] = t['temp_min']
    ans['Status'] = weather.get_detailed_status()
    ans['Sunrise'] = weather.get_sunrise_time('iso')
    ans['Sunset'] = weather.get_sunset_time('iso')
    ans['Humidity'] = weather.get_humidity()
    ans['Pressure'] = int(weather.get_pressure()['press'] / 1.3332239)
    ans['Wind'] = weather.get_wind()['speed']
    return ans


# построение графика по данным о температуре на ближайшие 5 дней
# сохраняем его как файл .png (после отправки сразу же удаляем)
def make_image(forecast, city):
    x_data = []
    y_data = []
    for weather in forecast:
        dt = str(weather.get_reference_time(timeformat='iso'))
        x_data.append(dt[8:10] + '.' + dt[5:7] + '\n' + dt[10:13] + ':00')
        y_data.append(int(weather.get_temperature(unit='celsius')['temp']))
    fig = plt.figure(figsize=(30, 15))
    ax = plt.axes()
    plt.plot(x_data, y_data)
    plt.style.use('seaborn-whitegrid')
    ax.set_title('Forecast in ' + city + ' for 5 days', size=25)
    ax.set_xlabel('date/time', size=20)
    ax.set_ylabel('temperature in Celsium', size=20)
    plt.savefig('images/graph' + city + '.png', format='png')


# оформляем обработанную информацию для ответа юзеру
def info(city):
    t_city = city
    raw_w, raw_f, country = get(city)
    w = format_weather(raw_w)
    make_image(raw_f, t_city)
    response = 'City: ' + str(t_city)
    if ',' not in t_city:
        response += ',' + country
    response += '\n'
    response += str(w['Status']) + '\n'
    response += 'Temperature: '
    if w['Current temperature'] > 0:
        response += '+'
    response += str(w['Current temperature']) + '\n'
    response += 'Wind: ' + str(w['Wind']) + ' m/s\n'
    response += 'Pressure: ' + str(w['Pressure']) + ' mmhg\n'
    response += 'Sunrise: ' + str(w['Sunrise']) + '\n'
    response += 'Sunset: ' + str(w['Sunset']) + '\n'
    return response, str(w['Status'])
