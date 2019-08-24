from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from pymongo import MongoClient
from datetime import date, datetime, timedelta
from crawler_combined import concert_ticket_data_list_crawler
import pprint

#today's date
today_int = date.today()
print("test_app - Today's date:", today_int)
today_str = str(today_int)

# mongodb setup
client = MongoClient('your_api_server_ip', 27017)
db = client.ukov_dev

alternative_calendar_col = db.calendar_alt.find()

def db_add_calendar_info_on(artist_name,calendar_id,crendential_id):
    db.calendar_alt.insert_one({'artist_name':artist_name,'calendar_id':calendar_id,'public_url':'https://calendar.google.com/calendar/embed?src='+calendar_id, 'credential_id':crendential_id,'input_date':today_str})


def one_artist_insert_cal_and_add_db(artist_name,credential_id):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    storage_location = credential_id +"/storage.json"
    store = file.Storage(storage_location)
    creds = store.get()

    if not creds or creds.invalid:
        print("no storage.json")
        credentials_location = credential_id + "/credentials.json"
        flow = client.flow_from_clientsecrets(credentials_location, SCOPES)
        creds = tools.run_flow(flow, store)

    service = discovery.build('calendar', 'v3', credentials=creds)

    # calendar information parameters
    calendar_info = {
        'summary': artist_name,
        'timeZone': 'Asia/Seoul'
    }

    # create calendar
    created_calendar = service.calendars().insert(body=calendar_info).execute()

    # created calendar's id
    print(created_calendar['id'])
    calendar_id = created_calendar['id']

    # save artist name and calendar id on mongodb
    db_add_calendar_info_on(artist_name,calendar_id,credential_id)

# one_artist_insert_cal_and_add_db('ADOY')

# testing whether it works or not for single item



def available_artist_list():
    concert_col = db.concert.find()
    avail_artist_list = []
    for concert_data in concert_col:
        artist_name = concert_data['artist_name']
        if artist_name not in avail_artist_list:
            avail_artist_list.append(artist_name)
    print(avail_artist_list)
    print(len(avail_artist_list))
    return avail_artist_list

# available_artist_list()

def chunks(list, length):
    """Yield successive n-sized chunks from l."""
    twentyfour_item_lists =[]
    for i in range(0, len(list), length):
        result = list[i:i + length]
        twentyfour_item_lists.append(result)
    return twentyfour_item_lists

# print(chunks(available_artist_list(),24))


# Python program to illustrate the intersection
# of two lists in most simple way
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def add_calendar_without_restriction():
    avail_artist_list = available_artist_list()
    avail_artist_list.remove('선우정아')
    twentyfour_item_lists = chunks(avail_artist_list,24)
    for item in twentyfour_item_lists[0]:
        one_artist_insert_cal_and_add_db(item,'')
    for item in twentyfour_item_lists[1]:
        one_artist_insert_cal_and_add_db(item,'')
    for item in twentyfour_item_lists[2]:
        one_artist_insert_cal_and_add_db(item,'')
    for item in twentyfour_item_lists[3]:
        one_artist_insert_cal_and_add_db(item,'')

# add_calendar_without_restriction()
