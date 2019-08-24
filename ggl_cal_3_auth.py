from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from pymongo import MongoClient
from datetime import date, datetime, timedelta
from crawler_combined import concert_ticket_data_list_crawler


#today's date
today_int = date.today()
print("test_app - Today's date:", today_int)
today_str = str(today_int)

# mongodb setup
db_client = MongoClient('your_api_server_ip', 27017)
db = db_client.ukov_dev


def authorizing_all_calendars():
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        print("no storage.json")
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = discovery.build('calendar', 'v3', credentials=creds)

    calendar_col = db.calendar.find()
    for data in calendar_col:
        calendar_id = data['calendar_id']
        rule = \
            {
        'scope':
            {
                'type': 'default'
            },
        'role': 'reader'
            }
        created_rule = service.acl().insert(calendarId=calendar_id, body=rule).execute()
        print(created_rule['id'])

# authorizing_all_calendars()

def authorizing_one_calendar(calendar_id):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        print("no storage.json")
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = discovery.build('calendar', 'v3', credentials=creds)

    rule = \
        {
    'scope':
        {
            'type': 'default',
            'value':'your_gmail_here'
        },
    'role': 'writer'
        }
    created_rule = service.acl().insert(calendarId=calendar_id, body=rule).execute()
    print(created_rule['id'])

