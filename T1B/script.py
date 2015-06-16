import requests
import datetime
import smtplib
from email.mime.text import MIMEText

woeid = '349859'  # Santiago
baseurl = 'https://query.yahooapis.com/v1/public/yql?q='
query = 'select item.forecast from weather.forecast where u="c" AND woeid=' + woeid
data_format = '&format=json'
data = requests.get(baseurl + query + data_format)
for item in data.json()['query']['results']['channel']:
    date = datetime.datetime.strptime(item['item']['forecast']['date'], '%d %b %Y')
    if date.date() == datetime.datetime.now().date():
        forecast = item['item']['forecast']

text_d = 'Santiago de Chile, ' + date.strftime('%d-%m-%Y') + ':\n\nHabrá una temperatura '
text_t = 'mínima de ' + forecast['low'] + '°C y una máxima de ' + forecast['high'] + '°C.'

string = text_d + text_t

msg = MIMEText(string)
msg['Subject'] = 'Pronóstico de hoy'
msg['From'] = 'pronosticoiic1005@gmail.com'
msg['To'] = 'rerrera.s@gmail.com'

s = smtplib.SMTP('smtp.gmail.com:587')
s.ehlo()
s.starttls()
username = 'pronosticoiic1005@gmail.com'
password = 'clave12345'
s.login(username, password)
s.send_message(msg)
s.quit()

# f = open('pronostico.txt', 'w')
# f.write(string)
# f.close()
