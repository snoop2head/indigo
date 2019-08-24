from pymongo import MongoClient
from datetime import date, datetime, timedelta

#today's date
today_int = date.today()
print("test_app - Today's date:", today_int)
today_str = str(today_int)

# mongodb setup
client = MongoClient('your_api_server_ip', 27017)
db = client.ukov_dev

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from crawler_combined import concert_ticket_data_list_crawler
from oauth2client.service_account import ServiceAccountCredentials


def crawl_and_google_calendar_writer(string_input):
    ticket_data_list = concert_ticket_data_list_crawler(string_input)
    #google calendar api authorization: scope and json key
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    GCAL = discovery.build('calendar', 'v3', http=creds.authorize(Http()))

    notification_list =[]
    for n in range(len(ticket_data_list)):
        #creating event based on dictionary format
        GMT_OFF = '+09:00'      # PDT/MST/GMT+9
        EVENT = {
            'summary': string_input + ": " + ticket_data_list[n]['title'],
            'start':  {'date': ticket_data_list[n]['start_date'], "timeZone": GMT_OFF},
            'end':    {'date': ticket_data_list[n]['end_date'], "timeZone": GMT_OFF},
            'description': "예매 링크: "+ ticket_data_list[n]['url'],
            'attendees': [
                {'email': 'friend1@example.com'},
                {'email': 'friend2@example.com'},
            ],
        }

        e = GCAL.events().insert(calendarId='primary',
                sendNotifications=True, body=EVENT).execute()

        print('''*** %r event added:
            Start: %s
            End:   %s''' % (e['summary'].encode('utf-8'),
                e['start']['date'], e['end']['date']))


def write_on_ggl_cal(artist_name,calendar_id,credential_id):
    #google calendar api authorization: scope and json key
    '''
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    GCAL = discovery.build('calendar', 'v3', http=creds.authorize(Http()))
    '''

    scope = ['https://www.googleapis.com/auth/calendar']
    credentials_location = credential_id + "/credentials.json"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_location, scope)
    GCAL = discovery.build('calendar', 'v3', http=credentials.authorize(Http()))

    #     일시적으로 db.concert로 세팅하겠음. 좀 있다가 notification이 오는지 테스트를 해야 하니까
    # 나중에는 db.archive로 바꿀 것!
    data_list = db.concert.find({'artist_name':artist_name})
    print(data_list)

    for data in data_list:
        print(data)
        #creating event based on dictionary format
        GMT_OFF = '+09:00'      # PDT/MST/GMT+9
        EVENT = {
            'summary': artist_name + ": " + data['title'],
            'start':  {'date': data['start_date'], "timeZone": GMT_OFF},
            'end':    {'date': data['end_date'], "timeZone": GMT_OFF},
            'description': "예매 링크: "+ data['url'],
        }
        e = GCAL.events().insert(calendarId=calendar_id,
                sendNotifications=True, body=EVENT).execute()

        print('''*** %r event added:
            Start: %s
            End:   %s''' % (e['summary'].encode('utf-8'),
                e['start']['date'], e['end']['date']))

def one_from_archive_db_to_ggl_cal(artist_name):
    data = db.calendar_alt.find_one({'artist_name':artist_name})
    print(data)
    calendar_id = data['calendar_id']
    print(calendar_id)
    credential_id = data['credential_id']
    write_on_ggl_cal(artist_name,calendar_id,credential_id)

# one_from_archive_db_to_ggl_cal('케이티')
# one_from_archive_db_to_ggl_cal('잔나비')
# one_from_archive_db_to_ggl_cal('김윤아')
# one_from_archive_db_to_ggl_cal('Cheeze')

def add_events_for_all_artists_on_ggl_cal():
    calendar_col = db.calendar_alt.find()
    newbies = db.calendar_alt.find({'event_written_date': {'$exists': False }})
    for newbie in newbies:
        print(newbie)
        artist_name = newbie['artist_name']
        calendar_id = newbie['calendar_id']
        credential_id = newbie['credential_id']
        print(str(newbie)+ 'has no event written on it')
        write_on_ggl_cal(artist_name,calendar_id,credential_id)
        db.calendar_alt.update_one(newbie,{'$set': {'event_written_date':today_str}})


add_events_for_all_artists_on_ggl_cal()



