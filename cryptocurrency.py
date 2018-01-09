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

import sys
import requests
from bs4 import BeautifulSoup

def get_status(rate):
    # Upcoming code

def main():
    try:
        REFRESH_RATE = int(sys.argv[1])
    except IndexError:
        print('Usage: cryptocurrency.py <argument>')
        sys.exit(1)
    except ValueError:
        print('Error: Argument provided is not an integer !! Try again.')
        sys.exit(2)


if __name__ == '__main__': main()
