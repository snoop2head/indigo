# Open_Race_of_Development_Indie_Band
- Don't miss any concerts for your favorite artists, with this KakaoTalk Chatbot.
  - [Click to see how it works](https://www.youtube.com/watch?v=uIOWqumaOD4)
- 공연 검색, 일정 확인 및 구글 캘린더 연동: 카카오 챗봇 "Indigo"
  - [(모바일 환경) 카카오톡 챗봇 시연 영상](https://www.youtube.com/watch?v=uIOWqumaOD4)



## Concert Information Selenium Crawler

- [x] [Make Interpark Ticket Information crawler for selected artist](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/crawler_interpark_ticket.py)
- [x] [Make Melon Ticket Information crawler for selected artist](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/crawler_melon_ticket.py)
- [x] [Combine two crawlers into one](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/crawler_combined.py)
- [x] [Update artist database daily](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/crawler_daily.py)



## [KakaoTalk Chatbot(Kakao Open Builder) Flask Server](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/app.py)

[You can also check for the server written in Node.js](https://github.com/PaperCrafter/IndiGo_APIServer)

- [x] Request: Receive User's Message 
  - [x] Receive Kakao user id (encrypted)
  - [x] Register user's favorite artists
- [x] Response: Send Artist's Concert information through KakaoTalk
  - [x] Send Horizontal arrays of carousel cards 
  - [x] Make button to the ticket information web link
  - [x] Make "Share to other friends in Kakao" button
  - [x] Sends "concert not found" message
  - [x] Sends concert schedules Google Calendar public web link
  - [x] [Checks for new ticket information and returns message](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/db_notify.py)



## MongoDB (Pymongo)

### User info

- [x] [Register user's favorite artists](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/db_user_interactions.py)
- [x] [Update user's favorite artists](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/db_user_interactions.py)

### Concert info

- [x] [Register Korean indie artists information from txt file](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/db_artists_registration.py)
- [x] [Register concert schedules for each artists](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/db_daily_sorter.py)
- [x] [Dump old concert information to old DB, update new concert information to current DB](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/db_daily_sorter.py)



## Visualize Concert Schedules with Google Calendar API 

- [x] [Make a Google Calendar page for each artists](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/ggl_cal_1_insert.py)
- [x] [Write concert schedules for each artists' Google Calendar page](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/ggl_cal_2_event_writer.py)
- [x] [Authorize Google Calendar page to public](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/ggl_cal_3_auth.py)
- [x] [Use Concert Crawler to update concert schedules on Google Calendar for each artists](https://github.com/snoop2head/Open_Race_of_Development_Indie_Band/blob/master/ggl_cal_9_get_and_update.py)



## 





