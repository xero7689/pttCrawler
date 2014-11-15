'''
pttCrawler Settings
'''
import os

# URL Setting
START_URL = "https://www.ptt.cc/bbs/Gossiping/index.html"
SITE = "https://www.ptt.cc"
OVER18 = "https://www.ptt.cc/ask/over18"

# DIR Setting
SAVE_DIR = "data"

# Working Path Setting
WORKING_PATH = os.path.dirname(os.path.abspath('__file__'))
SAVE_PATH = os.path.join(WORKING_PATH, SAVE_DIR)

# Crawler Setting
DELAY = 1
