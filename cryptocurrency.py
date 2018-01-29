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

DEFAULT_LTC = None

def set_default_price():
    global DEFAULT_LTC
    # For testing purpose, DEFAULT_LTC is set
    CurrentStatus = get_status() 
    print('Currently LTC price is at {} (INR) '.format(CurrentStatus[2]))
    DEFAULT_LTC = float(input('Enter LTC price that you want to watch: '))


def notify(price):
    toast = ToastNotifier()

    #Title of the notification
    title = 'LTC price: {}'.format(price)

    # Description of the notification of windows
    description = 'Look, there\'s a change in LTC price!'

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
    global DEFAULT_LTC
    price = get_status()
    print('-'*80)
    print('BTC: {}, BCH: {}, LTC: {} and DASH: {}'.format(*price))

    if DEFAULT_LTC < price[2]:
        DEFAULT_LTC = price[2]
        print(colored('*LTC price increased to {}'.format(DEFAULT_LTC), 'green'))
        alert.play()
        notify(DEFAULT_LTC)


def run(RATE):
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
