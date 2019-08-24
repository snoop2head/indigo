from pymongo import MongoClient
from datetime import date, datetime, timedelta
from db_daily_sorter import new_ticket_info_list, intersection

# time right now
now_int = datetime.now()
now_str = str(now_int)
print('daily crawler - Right now it is ' + now_str)

#today's date
date_today = date.today()
print("test_app - Today's date:", date_today)
today_str = str(date_today)

# mongodb setup
client = MongoClient('your_api_server_ip', 27017)
db = client.ukov_dev

# all data in user collection
user_db = db.user.find()

# sorting ticket data between concert_db and archive_db
# concert db is retrieving collection, archive db is accessing collection

'''
# initially adding dataset to archive_db
 for data in concert_db:
     db.archive.insert_one(data)
'''
def notify():
    # new ticket information list
    new_ticket_data_list = new_ticket_info_list()
    new_artist_list = []
    user_package_list = []

    # find Intersection of two lists: new ticket data list and user subscribed artist list
    for new_ticket_data in new_ticket_data_list:
        candidate_artist = new_ticket_data['artist_name']
        # print(candidate_artist)
        new_artist_list.append(candidate_artist)
    for user in user_db:
        usr_subscrib_artist_list = user['subscribed_artist_list']
        artist_list = intersection(new_artist_list,usr_subscrib_artist_list)
        # print(artist_list)

        # make package of {user_key, new_ticket_data}
        if artist_list:
            for artist in artist_list:
                for new_ticket_data in new_ticket_data_list:
                    candidate_artist = new_ticket_data['artist_name']
                    # print(candidate_artist)
                    if artist == candidate_artist:
                        user_package = {'user_key':user['user_key'],'new_info':new_ticket_data}
                        user_package_list.append(user_package)
                    else:
                        pass
        else:
            pass
    print(user_package_list)
    return user_package_list

'''
def notify():
    new_ticket_data_list = new_ticket_info_list()
    for user in user_db:
        usr_subscrib_artist_list = user['subscribed_artist_list']
        matches = []
        # print(usr_subscrib_artist_list)
        # for artist in usr_subscrib_artist_list:
        for new_ticket_data in new_ticket_data_list:
            candidate_artist = new_ticket_data['artist_name']
            if candidate_artist in usr_subscrib_artist_list:
                matches.append(candidate_artist)
                print(matches)
            else:
                pass
'''

notify()
