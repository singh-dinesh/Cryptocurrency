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

# For testing purpose, DEFAULT_LTC is set
DEFAULT_LTC = 17000.0

def notify(price):
    toast = ToastNotifier()

    #Title of the notification
    title = 'LTC price rose to {}'.format(price)

    # Description of the notificatio of windows
    description = 'For best profit, buy if price below 17000'

    # Display the notification
    toast.show_toast(title, description)

# What's the current cryptocurrency status, fetch it for me -> get_status()
def get_status():
    URL = 'https://www.coinome.com/exchange'
    content = requests.get(URL).content
    soup = BeautifulSoup(content, 'html.parser')

    Currencies = soup.findAll('span', {'class': 'last-market-rate-b'})
    price = []
    for currency in Currencies:
        price.append(float(currency.text.replace(',','')))

    print('-'*80)
    print('BTC: {}, BCH: {} and LTC: {}'.format(*price))

    global DEFAULT_LTC
    if DEFAULT_LTC < price[2]:
        DEFAULT_LTC = price[2]
        print(colored('*LTC price increased to {}'.format(price[2]), 'green'))
        alert.play()
        notify(DEFAULT_LTC)


def run(RATE):
    print(colored('Getting Current Status:', 'green'))
    print("o_o Watching LTC")
    while True:
        try:
            get_status()
            time.sleep(RATE)
        except:
            print('Trying to reconnect...')
            time.sleep(10)


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
