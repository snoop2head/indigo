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


def authorizing_one_calendar(calendar_id,credential_id):
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

    rule = \
        {
    'scope':
        {
            'type': 'default',
            'value':credential_id
        },
    'role': 'writer'
        }
    created_rule = service.acl().insert(calendarId=calendar_id, body=rule).execute()
    print(created_rule['id'])

def auth_calendar_without_restriction():
    calendar_col = db.calendar_alt.find()
    newbies = db.calendar_alt.find({'event_auth_date': {'$exists': False }})
    for newbie in newbies:
        print(newbie)
        calendar_id = newbie['calendar_id']
        credential_id = newbie['credential_id']
        print(str(newbie)+ 'has no event written on it')
        authorizing_one_calendar(calendar_id,credential_id)
        db.calendar_alt.update_one(newbie,{'$set': {'event_auth_date':today_str}})
