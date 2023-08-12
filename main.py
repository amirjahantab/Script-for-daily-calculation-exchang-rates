from datetime import datetime

import requests
import json

from khayyam import JalaliDatetime

from config import url, rules
from mail import send_smtp_email
from notification import send_sms


def get_rates():
    """
    send a get requests to the fixer.io api and get live rates
    :return: request.Response instance
    """
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    return None


def archive(filename, rates):
    """
    get filename and rates, save them to the specific directory
    :param filename:
    :param rates:
    :return: None
    """
    with open(f'archive/{filename}.json', 'w') as f:
        f.write(json.dumps(rates))


def send_mail(timestamp, rates):
    """
    get timestamp and rates, check if there is preferred rates and
    then send email through smtp
    :param timestamp:
    :param rates:
    :return:
    """
    now = JalaliDatetime(datetime.now()).strftime('%y-%B-%d  %A  %H:%M')
    subject = f"{timestamp} - {now} - rates"

    if rules['email']['preferred'] is not None:
        tmp = dict()
        for exc in rules['email']['preferred']:
            tmp[exc] = rates[exc]
        rates = tmp

    text = json.dumps(rates)

    send_smtp_email(subject, text)


def check_notify_rules(rates):
    """
    Check if user defined notify rules and if rates reached to the defined
    rules, then generate proper msg to send.
    :param rates:
    :return: msg (str)
    """
    preferred = rules['notification']['preferred']
    msg = ''
    for exc in preferred.keys():
        if rates[exc] <= preferred[exc]['min']:
            msg += f'{exc} reached min: {rates[exc]} \n'
        if rates[exc] >= preferred[exc]['max']:
            msg += f'{exc} reached max: {rates[exc]} \n'

    return msg


def send_notification(msg):
    now = JalaliDatetime(datetime.now()).strftime('%y-%B-%d  %A  %H:%M')
    msg += now
    send_sms(msg)


if __name__ == "__main__":
    res = get_rates()

    if rules['archive']:
        archive(res['timestamp'], res['rates'])

    if rules['email']['enable']:
        send_mail(res['timestamp'], res['rates'])

    if rules['notification']['enable']:
        notification_msg = check_notify_rules(res['rates'])
        if notification_msg:
            send_notification(notification_msg)
