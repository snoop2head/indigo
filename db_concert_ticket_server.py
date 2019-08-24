from pymongo import MongoClient
from datetime import date, datetime, timedelta

#today's date
today_int = date.today()
today_str = str(today_int)

#mongodb setup
client = MongoClient('your_api_server_ip',27017)
db = client.ukov_dev

#settingup concert db
concert_db = db.concert.find()


def concert_ticket_data_to_concert_db(concert_ticket_data_data_list):
  # sample list is following:
  # returns list of data
  # data format is {artist_name, title, url, start_date, end_date, crawled_date}
  for data in concert_ticket_data_data_list:
    db.concert.insert_one(data)
  print("db_server - " + str(len(concert_ticket_data_data_list))+" of items are added to concert_ticket_db")




