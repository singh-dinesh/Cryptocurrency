#!usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = ['Dinesh Singh']
__version__ = '1.0.0'
__copyright__ = 'Copyright (c) 2017-2018 Dinesh Singh'
__license__ = 'MIT'

"""
A short module that can save your precious time that you spend checking the
right time to buy a cryptocurrency.
"""
import requests
import sys, time
from pygame import mixer
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

# Initialized the mixer object
mixer.init()
alert=mixer.Sound('./assets/bell.wav')

choice = None
DEFAULT_CURRENCY = None
CURRENCIES = {'BTC': 0, 'BCH': 1 , 'LTC': 2, 'DASH': 3, 'DGB': 4, 'ZEC'}

def set_currency():
    global choice, DEFAULT_CURRENCY
    available_currencies = ('BTC', 'BCH', 'LTC', 'DASH', 'DGB', 'ZEC')
    print('Hi! Choose your currency? (BTC/BCH/LTC/DASH/DGB/ZEC) >>', end=' ')
    choice = input().strip().upper()
    if choice in available_currencies:
        DEFAULT_CURRENCY = 0.0


def set_default_price():
    global DEFAULT_CURRENCY
    current_status = get_status()
    choice_index = CURRENCIES.get(choice)
    print('Currently {} price is at {} (INR) '.format(choice, current_status[choice_index]))
    DEFAULT_CURRENCY = float(input('Enter {} price that you want to watch: '.format(choice)))


def notify(price):
    toast = ToastNotifier()

    #Title of the notification
    title = ' {} rose to: Rs {}'.format(choice, DEFAULT_CURRENCY)

    # Description of the notification of windows
    description = 'Current Prices: (In INR)\n\
BTC : {}  \t    BCH : {}  \n\
LTC : {}  \t    DASH : {} \n\
DGB : {}  \t    ZEC : {} \
    '.format(*price)

    # Notification icon
    icon = './assets/icon.ico'
    
    # Time period of the notification
    time = 20

    # Display the notification
    toast.show_toast(title, description, icon, time)

# What's the current cryptocurrency status, fetch it for me -> get_status()
def get_status():
    URL = 'https://www.coinome.com/exchange'
  
    try:
        content = requests.get(URL).content
    except:
        print('Trying to reconnect...')
        time.sleep(10)

    soup = BeautifulSoup(content, 'html.parser')

    Currencies = soup.findAll('span', {'class': 'last-market-rate-b'})
    price = []
    for currency in Currencies:
        price.append(float(currency.text.replace(',', '')))

    return price

# Print the fetched status
def print_status():
    global DEFAULT_CURRENCY
    price = get_status()
    choice_index = CURRENCIES.get(choice)
    currency_current_price = price[choice_index]
    print('-'*80)
    print('BTC: {}, BCH: {}, LTC: {}, DASH: {}, DGB: {} and ZEC: {}'.format(*price))

    if DEFAULT_CURRENCY < currency_current_price:
        DEFAULT_CURRENCY = currency_current_price
        print('*{} price increased to {}'.format(choice, DEFAULT_CURRENCY))
        alert.play()
        notify(price)


def run(RATE):
    set_currency()
    set_default_price()
    print('\n\nGetting Current Status:')
    print("o_o Watching {}\n".format(choice))
    while True:
        print_status()
        time.sleep(RATE)
            

def main():
    try:
        if len(sys.argv) > 2:
            raise IndexError()
        REFRESH_RATE = int(sys.argv[1])
        run(REFRESH_RATE)
    except IndexError:
        print('Usage: cryptocurrency.py <argument>')
    except ValueError:
        print('Error: Argument provided is not an integer !! Try again.')


if __name__ == '__main__': main()
