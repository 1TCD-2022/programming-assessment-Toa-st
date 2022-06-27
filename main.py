"""
Filename: main.py
Author: Varun Goel
Date: 27 / 06 / 22
Description: 
Version: 1.0
"""

import gspread
import json

RAW_LOGIN_DETAILS = open('config.json')
LOGIN_DETAILS = json.load(RAW_LOGIN_DETAILS)

print(LOGIN_DETAILS)
