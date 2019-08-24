# -*- coding: utf-8 -*-

from db_concert_ticket_server import concert_ticket_data_to_concert_db
from crawler_combined import concert_ticket_data_list_crawler
from pymongo import MongoClient
from datetime import date, datetime, timedelta

# time right now
now_int = datetime.now()
now_str = str(now_int)
print('daily crawler - Right now it is ' + now_str)

# mongodb setup
client = MongoClient('your_api_server_ip', 27017)
db = client.ukov_dev

# establishing artist db collection
artist_db = db.artist.find()

print(artist_db)


# crawling ticket data to concert_db


def update_concert_col():
    # drop the concert db
    db.concert.drop()

    for artist_data in artist_db:
        artist_name = artist_data['artist_name']
        concert_ticket_data_list = concert_ticket_data_list_crawler(artist_name)
        concert_ticket_data_to_concert_db(concert_ticket_data_list)

# update_concert_col()


def individual_crawling(artist_name):
    concert_ticket_data_list = concert_ticket_data_list_crawler(artist_name)
    concert_ticket_data_to_concert_db(concert_ticket_data_list)

# mongodb는 100개 아이템밖에 하지 못한다!
def crawl_the_rest():
    list = ['artist1','artist2']
    for artist_name in list:
        individual_crawling(artist_name)

crawl_the_rest()
