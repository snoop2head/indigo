# Based on user input from Kakao
# add new artist on artist_db
# add or update user infromation on user_db
# add concert information on concert_db

from pymongo import MongoClient
from datetime import date, datetime, timedelta


#today's date
today_int = date.today()
print("test_app - Today's date:", today_int)
today_str = str(today_int)

#mongodb setup
client = MongoClient('your_api_server_ip',27017)
db = client.ukov_dev

'''
#establishing concert db collection
concert_db = db.concert.find()

#establishing artist db collection
artist_db = db.artist.find()

#establishing user db collection
user_db = db.user.find()
'''

def user_respond(user_given_artist_name,user_input_time,user_key):

  # insert user_given_artist_name to artist_db
  # data format is {user_key, subscribed_artist_list, user_input_time}
  user_mongodb_data = db.user.find_one({'user_key':user_key})

  if not user_mongodb_data:
      #if user is new, add a user data in user db
      db.user.insert_one({'user_key':user_key,'subscribed_artist_list':[user_given_artist_name],'registered_date':[user_input_time]})
  else:
      subscribed_artist_list = user_mongodb_data['subscribed_artist_list']
      if user_given_artist_name in subscribed_artist_list:
          pass
      else:
          #if previous user inputs new artist name into subscribed_artist_list
          #appending in mongodb is $push
          db.user.update_one({'user_key':user_key},{'$push': {'subscribed_artist_list':user_given_artist_name,'registered_date':user_input_time}})

  # data format is {artist_name, registered_date, [user_key1, user_key2, user_key3 ...]}
  # data format will be changed to {artist_name, registered_date, user_key_list, no_available concerts}
  artist_mongodb_data = db.artist.find_one({'artist_name':user_given_artist_name})
  print("test_app - archived mongodb data is" + str(artist_mongodb_data))

  # find first data of the artist in artist db
  if artist_mongodb_data:
      print("test_app - artist " + artist_mongodb_data['artist_name'] + " already exists on artist_db")
      if user_key in artist_mongodb_data['user_key_list']:
          pass
      #add user information as a subscriber to artist db
      else:
          db.artist.update_one({'artist_name':user_given_artist_name},{'$push': {'registered_date':user_input_time,'user_key_list':user_key}})

  # crawling for new artist, but it is yet to function
  else:
      print("test_app - new artist information: " + user_given_artist_name)
      print("test_app - new artist " + user_given_artist_name + " is added on artist_db")

      # crawling for new artist function does not exist
      # data format is {artist_name, title, url, start_date, end_date, crawled_date}
      #if concert_ticket_mongo_db_data is Nonetype then insert crawled concert ticket data to db

      #add number of available tickets to artist db
      # data format is {artist_name, registered_date, user_key_list}
      db.artist.insert_one({'artist_name':user_given_artist_name,'registered_date':[user_input_time],'user_key_list':[user_key]})
