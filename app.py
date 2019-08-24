from flask import Flask, request, jsonify
from db_user_interactions import user_respond
from pymongo import MongoClient
from datetime import date, datetime, timedelta
import re

#today's date
today_int = date.today()
print("test_app - Today's date:", today_int)
today_str = str(today_int)

#mongodb setup
client = MongoClient('your_api_server_ip',27017)
db = client.ukov_dev

# app is Flask
app = Flask(__name__)

'''
data_list = db.archive.find({'artist_name':'새소년'})
for data in data_list:
    print(data)
'''

@app.route('/', methods=['POST'])
def receive_message():
    # data received from KakaoTalk
    dataReceive = request.get_json()
    print(dataReceive)

    user_key = dataReceive["userRequest"]["user"]["id"]
    print(user_key)

    # json format is 'userRequest' -> 'utterance'
    if dataReceive["userRequest"]["utterance"]:
        # received name
        # name = dataReceive["userRequest"]["utterance"]
        # user request refining artist
        # db.same_name.find_one('name')

        # registered name
        artist_name = dataReceive["action"]["params"]["가수"]
        print("processing name is "+ artist_name)
        # need to extract the text getting rid of \n and ]r
        if re.search("(\\r|)\\n$", artist_name):
            artist_name= re.sub("(\\r|)\\n$", "", artist_name)
        data_list = db.archive.find({'artist_name':artist_name})
        print("app.py - data list from archive is:" + str(data_list))
        item_list =[]
        # find all data from archive collection
        # if there is ticket information on archive
        # getting user key and registering on db
        user_respond(artist_name, today_str, user_key)

        for data in data_list:
            duration = "기간: " + data['start_date'] + " ~ " + data['end_date']
            item = \
            {
                "title":data['title'],
                "description":duration,
                "thumbnail":
                    {
                        "imageUrl":data['poster_png']},
                        "social": {"like":"","comment":"","share":""},
                        "buttons":
                          [{"action":"webLink","label":"예매하기",
                            "webLinkUrl":data['url']},
                            {"action":"share","label":"공유하기"}]
             }
            item_list.append(item)

        if not item_list:
            dataSend = {
            "version": "2.0",
            "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "ㅠㅠ "+artist_name+"의 공연이 안 잡혔나봐요 ㅠㅠ"
                    }
                }
                ]
            }}

            return jsonify(dataSend)
        else:
            # changed "Carousel" into "carousel"
            dataSend = \
                {"version":"2.0",
                 "template":
                     {"outputs":
                          [{"carousel":
                                {"type":"basicCard","items": item_list}}]}}

            print(dataSend)
            return jsonify(dataSend)


@app.route('/calendar', methods = ['POST'])
def receive_for_calendar():
    # data received from KakaoTalk
    dataReceive = request.get_json()
    print(dataReceive)

    user_key = dataReceive["userRequest"]["user"]["id"]
    print(user_key)

    # json format is 'userRequest' -> 'utterance'
    if dataReceive["userRequest"]["utterance"]:
        # received name
        # name = dataReceive["userRequest"]["utterance"]
        # user request refining artist
        # db.same_name.find_one('name')

        # registered name
        artist_name = dataReceive["action"]["params"]["가수"]
        print("processing name is "+ artist_name)
        # need to extract the text getting rid of \n and ]r
        if re.search("(\\r|)\\n$", artist_name):
            artist_name= re.sub("(\\r|)\\n$", "", artist_name)
        public_url_data = db.calendar.find_one({'artist_name':artist_name})
        if not public_url_data:
            dataSend = {
            "version": "2.0",
            "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "ㅠㅠ "+artist_name+"의 공연이 안 잡혔나봐요 ㅠㅠ"
                    }
                }
                ]
            }}

            return jsonify(dataSend)
        else:
            public_url = public_url_data['public_url']
            print(public_url)
            dataSend = \
            {"version":"2.0",
              "template":
              {
                "outputs":
                [
                  {
                    "basicCard":
                    {
                      "title":"",
                      "description":"공연일정을 달력으로 보시겠습니까?",
                      "thumbnail":{},
                      "social":
                      {
                        "like":"",
                        "comment":"",
                        "share":"",
                      },
                      "buttons":
                      [
                        {"action":"webLink",
                          "label":"달력으로 보기",
                          "webLinkUrl":public_url,
                        }
                      ],
                    },
                  }
                ],
              },
            }

            print(dataSend)
            return jsonify(dataSend)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)


'''
# sample from Kakao instruction
# https://i.kakao.com/docs/skill-response-format#bot
dataSend = {
          "version": "2.0",
          "template": {
            "outputs": [
              {
                "carousel": {
                  "type": "basicCard",
                  "items": [
                    {
                      "title": "보물상자",
                      "description": "보물상자 안에는 뭐가 있을까",
                      "thumbnail": {
                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                      },
                      "buttons": [
                        {
                          "action": "message",
                          "label": "열어보기",
                          "messageText": "짜잔! 우리가 찾던 보물입니다"
                        },
                        {
                          "action":  "webLink",
                          "label": "구경하기",
                          "webLinkUrl": "https://e.kakao.com/t/hello-ryan"
                        }
                      ]
                    },
                    {
                      "title": "보물상자2",
                      "description": "보물상자2 안에는 뭐가 있을까",
                      "thumbnail": {
                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                      },
                      "buttons": [
                        {
                          "action": "message",
                          "label": "열어보기",
                          "messageText": "짜잔! 우리가 찾던 보물입니다"
                        },
                        {
                          "action":  "webLink",
                          "label": "구경하기",
                          "webLinkUrl": "https://e.kakao.com/t/hello-ryan"
                        }
                      ]
                    },
                    {
                      "title": "보물상자3",
                      "description": "보물상자3 안에는 뭐가 있을까",
                      "thumbnail": {
                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                      },
                      "buttons": [
                        {
                          "action": "message",
                          "label": "열어보기",
                          "messageText": "짜잔! 우리가 찾던 보물입니다"
                        },
                        {
                          "action":  "webLink",
                          "label": "구경하기",
                          "webLinkUrl": "https://e.kakao.com/t/hello-ryan"
                        }
                      ]
                    }
                  ]
                }
              }
            ]
          }
                    }
'''
