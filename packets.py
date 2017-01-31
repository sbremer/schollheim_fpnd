import requests
import re
import time
import sys
import smtplib
import datetime
from email.mime.text import MIMEText

# Load config
import config
users_config = config.users_config
email_config = config.email_config
timeout = config.timeout

initial = True


def send_mail(to, title, content):
    msg = MIMEText(content)

    msg['Subject'] = title
    msg['From'] = email_config['from']
    msg['To'] = to

    s = smtplib.SMTP(email_config['server'], email_config['port'])
    s.starttls()
    s.login(email_config['auth_user'], email_config['auth_passwd'])
    s.sendmail(email_config['from'], [to], msg.as_string())
    s.quit()


def notify(user, date, n, mail_to):

    if n is '':
        n = '1'
        s = ''
    else:
        s = 's'

    print('Notifying user {} about {} new package{} on day {}'.format(user, n, s, date))
    title = 'Schollheim: {} new package{} on {} for {}'.format(n, s, date, user)
    content = 'You have received {} new package{} on {}. Pick them up from the Verwaltung.'.format(n, s, date)
    send_mail(mail_to, title, content)


def main():
    global initial
    url = 'http://192.168.34.73/intern/verwaltung/packchen-pakete'
    regex_date = r'<strong>(.+?)</strong>'

    users = users_config.keys()

    users_dates = {}
    for user in users:
        users_dates[user] = []

    while True:
        try:
            req = requests.get(url)
            print('Successful pull at {}          '.format(datetime.datetime.now().time()), end='\r', flush=True)
        except:
            print('Request failed at {}           '.format(datetime.datetime.now().time()), end='\r', flush=True)
            time.sleep(timeout)
            continue
        
        htmldata = req.text

        for user in users:

            regex_user = '{}(.*?)<br />'.format(user)
            findings = [(m.start(0), m.group(0)) for m in re.finditer(regex_user, htmldata)]

            dates = []

            for find, text in findings:
                # print(find, text)
                date = re.findall(regex_date, htmldata[:find])[-1].replace('<br />', '')
                n = text.replace(user, '').replace('x', '').replace('<br />', '').replace(' ', '')

                if date not in users_dates[user] and not initial:
                    notify(user, date, n, users_config[user])

                dates.append(date)

            users_dates[user] = dates

        initial = False
        time.sleep(timeout)

if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        initial = False
    else:
        initial = True

    main()




