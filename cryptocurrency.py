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
from termcolor import colored
from win10toast import ToastNotifier

# Initialized the mixer object
mixer.init()
alert=mixer.Sound('bell.wav')

choice = None
DEFAULT_CURRENCY = None
CURRENCIES = {'BTC': 0, 'BCH': 1 , 'LTC': 2, 'DASH': 3}

def set_currency():
    global choice, DEFAULT_CURRENCY
    available_currencies = ('BTC', 'BCH', 'LTC', 'DASH')
    print('Hi! Choose your currency? (BTC/BCH/LTC/DASH) >>', end=' ')
    choice = input().strip().upper()
    if choice in available_currencies:
        DEFAULT_CURRENCY = 0.0


def set_default_price():
    global DEFAULT_CURRENCY
    # For testing purpose, DEFAULT_CURRENCY is set
    current_status = get_status()
    choice_index = CURRENCIES.get(choice)
    print('Currently {} price is at {} (INR) '.format(choice, current_status[choice_index]))
    DEFAULT_CURRENCY = float(input('Enter {} price that you want to watch: '.format(choice)))
    

def notify(price):
    toast = ToastNotifier()

    #Title of the notification
    title = 'LTC price: {}'.format(price)

    # Description of the notification of windows
    description = 'Look, there\'s a change in {} price!'.format(choice)

    # Display the notification
    toast.show_toast(title, description)

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
        price.append(float(currency.text.replace(',','')))

    return price

# Print the fetched status
def print_status():
    global DEFAULT_CURRENCY
    price = get_status()
    print('-'*80)
    print('BTC: {}, BCH: {}, LTC: {} and DASH: {}'.format(*price))

    if DEFAULT_CURRENCY < price[2]:
        DEFAULT_CURRENCY = price[2]
        print(colored('*LTC price increased to {}'.format(DEFAULT_CURRENCY), 'green'))
        alert.play()
        notify(DEFAULT_CURRENCY)


def run(RATE):
    set_currency()
    set_default_price()
    print(colored('\nGetting Current Status:', 'green'))
    print("o_o Watching LTC")
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
