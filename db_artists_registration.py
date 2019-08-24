#-*- coding:utf-8 -*-
from pymongo import MongoClient
from datetime import date, datetime, timedelta
from db_user_interactions import user_respond
import re

#today's date
today_int = date.today()
print("test_app - Today's date:", today_int)
today_str = str(today_int)

#mongodb setup
client = MongoClient('your_api_server_ip',27017)
db = client.ukov_dev
'''
db.artist.drop()
'''

# db initializing
# csv에서 ctrl c + ctrl v로 txt파일에 갖다 붙이고, 각 줄마다 읽어서 리스트 만드는 것.
with open('machine-learning.txt', 'rt', encoding='UTF8') as f:
    lis = [re.sub("(\\r|)\\n$", "", line) for line in f]        # create a list of lists
    print(lis)

list = ['선우정아', '새소년']

date_list = []
date_list.append(today_str)

for i in lis:
    user_respond(i,today_str,'asd123')
