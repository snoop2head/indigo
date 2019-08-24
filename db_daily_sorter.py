from pymongo import MongoClient
from datetime import date, datetime, timedelta

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

# all data in archive collection
archive_db = db.archive.find()

# all data in concert collection
concert_db = db.concert.find()

# sorting ticket data between concert_db and archive_db
# concert db is retrieving collection, archive db is accessing collection

'''
# initially adding dataset to archive_db
 for data in concert_db:
     db.archive.insert_one(data)
'''

#delete outdated data from archive collection
#add outdated data to old collection

def sort_out_old_tickets():
    for data in archive_db:
        str_start_date = data['start_date']
        # print(str_start_date)
        #converting start_date string into date format
        y1, m1, d1 = [int(x) for x in str_start_date.split('-')]
        date_start_date = date(y1, m1, d1)


        if date_start_date > date_today:
            print("db_daily_sorter - this data is still valid " + str(data))
            pass
        else:
            print("db_daily_sorter - this data is outdated: " + str(data))
            db.old.insert_one(data)
            db.archive.delete_one(data)

def new_ticket_info_list():
    new_ticket_info_list = []
    for data in concert_db:
        index_url = data['url']
        existed_archive_data = db.archive.find_one({'url':index_url})
        '''
        # 만약 같은 페스티벌에 같은 가수가 두 명이 등장하면, 같은 데이터로 인지를 한다.
        # 그러면 공연정보가 있어도 어떤 아티스트는 추가가 되고, 어떤 아티스트는 추가가 안 된다. 
        # 따라서 가수 이름 + URL을 붙인 인덱스를 새로 만든다.
        # 아니면 크롤링 로직을 새로 짜서 가수 정보가 많은 경우는 한꺼번에 등록하게 할까? 
        
        
        artist_name = data['artist_name']
        index_concert = artist_name + data['url']
        index_archive = existed_archive_data['artist_name'] + existed_archive_data['url']
        '''
        if existed_archive_data:
            # print("db_daily_sorter - existing concert information")
            pass
        else:
            print("db_daily_sorter - this is new data: " + str(data))
            new_ticket_info_list.append(data)
    print(new_ticket_info_list)
    print(len(new_ticket_info_list))
    return new_ticket_info_list


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def update_archive_db():
    new_data_list = new_ticket_info_list()
    for data in new_data_list:
        db.archive.insert_one(data)
        print(str(data) + ' is updated')

sort_out_old_tickets()
update_archive_db()
