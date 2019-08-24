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
client = MongoClient('your_api_server_ip', 27017)
db = client.ukov_dev



# get all created calendars' id from the creator's calendar list
def get_all_calendars_id():
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        print("no storage.json")
        flow = client.flow_from_clientsecrets('client_secret_calendar.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = discovery.build('calendar', 'v3', credentials=creds)

    page_token = None
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        print(calendar_list_entry['summary'])
        print(calendar_list_entry['id'])
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break

    result = service.calendarList().list().execute()
    print(result)

# updating specific calendar
def update_calendar(calendar_id):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        print("no storage.json")
        flow = client.flow_from_clientsecrets('client_secret_calendar.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = discovery.build('calendar', 'v3', credentials=creds)

    # First retrieve the calendar from the API.
    calendar = service.calendars().get(calendarId=calendar_id).execute()

    # changing the title of the calendar
    calendar['summary'] = 'ADOY 밴드'
    updated_calendar = service.calendars().update(calendarId=calendar_id, body=calendar).execute()


