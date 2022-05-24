from flask import Blueprint
from flask import Flask, request, jsonify
import pandas as pd

# ----- house_welfare blueprint set ----------------------------------------------------------------------------
blue_house_welfare = Blueprint("house_welfare", __name__, url_prefix='/house_welfare')
#---------------------------------------------------------------------------------------------------------------

# ----- house_welfare root -------------------------------------------------------------------------------------
@blue_house_welfare.route("/")
def house_welfare_home():
    return "house_welfare"
# --------------------------------------------------------------------------------------------------------------

# ----- house_welfare/info_des ---------------------------------------------------------------------------------
@blue_house_welfare.route("/info_des", methods=['POST'])
def house_welfare_info_des():
    body = request.get_json()
    
    welfare_info_house = pd.read_csv("./data/welfare_info/housing_welfare_service.csv")
    
    welfare_dict = {'total-public-des' : 0, 'per-lease-des' : 1, 'happy-house-des': 2, 
                    'deposit-lease-des': 3, 'purchase-lease-des' : 4, 'kukmin-lease-des' : 5, 
                    'public-support-des' : 6, 'dwelling-welfare-des': 7, 'public-dormitory-des' : 8, 
                    'long-deposit-des' : 9, 'public-lease-des':10}
    
    index_num = welfare_dict[body['intent']['name']]

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(welfare_info_house.iloc[index_num]['title']) + "\n\n" 
                                + str(welfare_info_house.iloc[index_num]['describe'])
                    }
                }
            ],
            "quickReplies": [
                {
                "label": "상세정보",
                "action": "block",
                "blockId": "628af60133d26f492e9ec5be",
                "extra": {"welfare_type" : str(welfare_info_house.iloc[index_num]['title'])}
                },
                {
                "label": "주택복지",
                "action": "block",
                "blockId": "62859d5e33d26f492e9e84ed"
                },
                {
                "label": "메인메뉴",
                "action": "block",
                "blockId": "62873757ee5923754330c0b2"
                }
            ]
        }
    }

    return responseBody
# --------------------------------------------------------------------------------------------------------------

# ----- house_welfare/info -------------------------------------------------------------------------------------
@blue_house_welfare.route("/info", methods=['GET', 'POST'])
def housing_welfare():
    req = request.get_json()
    
    welfare_info_house = pd.read_csv("./data/welfare_info/housing_welfare_service.csv")
    
    #json 파일 읽기
    #house_welfare = req["action"]["detailParams"]["welfare_type"]["value"]
    
    #answer = house_welfare
    
    #답변 텍스트 설정
    res = {
  "version": "2.0",
  "template": {
    "outputs": [
        {
            "simpleText": {
                "text": "10가지의 주거복지 서비스가 존재합니다. 원하시는 서비스를 선택하세요"
            }
          },
      {
        "carousel": {
          "type": "itemCard",
          "items": [
            {
              "imageTitle": {
                "title": "통합공공임대주택",
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[0]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[0]['term']
                },
                {
                  "title" : "전용면적",
                  "description" : welfare_info_house.iloc[0]['dedicated_area']
                },
                {
                  "title" : "임대조건",
                  "description" : welfare_info_house.iloc[0]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : "6285ee6d33d26f492e9e91a9",
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide=RH112"
                }
              ]
            },
            {
              "imageTitle": {
                "title": "영구임대주택",
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[1]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[1]['term']
                },
                {
                  "title" : "전용면적",
                  "description" : welfare_info_house.iloc[1]['dedicated_area']
                },
                {
                  "title" : "임대조건",
                  "description" : welfare_info_house.iloc[1]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : "62870b8033d26f492e9ea196"
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide=RH103"
                }
              ]
            },
            {
              "imageTitle": {
                "title": "국민임대주택",
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[2]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[2]['term']
                },
                {
                  "title" : "전용면적",
                  "description" : welfare_info_house.iloc[2]['dedicated_area']
                },
                {
                  "title" : "임대조건",
                  "description" : welfare_info_house.iloc[2]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : "62870c5875eca02fba63dd20"
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide=RH104"
                }
              ]
            },
            {
              "imageTitle": {
                "title": "장기전세주택",
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[9]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[9]['term']
                },
                {
                  "title" : "전용면적",
                  "description" : welfare_info_house.iloc[9]['dedicated_area']
                },
                {
                  "title" : "임대조건",
                  "description" : welfare_info_house.iloc[9]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : "62870c9f33d26f492e9ea1cd"
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide=RH105"
                }
              ]
            },
            {
              "imageTitle": {
                "title": "공공임대주택",
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[10]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[10]['term']
                },
                {
                  "title" : "전용면적",
                  "description" : welfare_info_house.iloc[10]['dedicated_area']
                },
                {
                  "title" : "임대조건",
                  "description" : welfare_info_house.iloc[10]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : "62870cbaee5923754330b909"
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide=RH106"
                }
              ]
            },
            {
              "imageTitle": {
                "title": "전세임대주택",
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[3]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[3]['term']
                },
                {
                  "title" : "전용면적",
                  "description" : welfare_info_house.iloc[3]['dedicated_area']
                },
                {
                  "title" : "임대조건",
                  "description" : welfare_info_house.iloc[3]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : "62870be275eca02fba63dd07"
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide=RH107"
                }
              ]
            },
            {
              "imageTitle": {
                "title": "행복주택",
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[2]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[2]['term']
                },
                {
                  "title" : "전용면적",
                  "description" : welfare_info_house.iloc[2]['dedicated_area']
                },
                {
                  "title" : "임대조건",
                  "description" : welfare_info_house.iloc[2]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : "62870bce33d26f492e9ea1a3"
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide=RH108"
                }
              ]
            },
            {
              "imageTitle": {
                "title": "공공지원민간임대주택",
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[6]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[6]['term']
                },
                {
                  "title" : "전용면적",
                  "description" : welfare_info_house.iloc[6]['dedicated_area']
                },
                {
                  "title" : "임대조건",
                  "description" : welfare_info_house.iloc[6]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : "62870c6bee5923754330b8f7"
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide=RH109"
                }
              ]
            },
            {
              "imageTitle": {
                "title": "주거복지동주택",
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[7]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[7]['term']
                },
                {
                  "title" : "전용면적",
                  "description" : welfare_info_house.iloc[7]['dedicated_area']
                },
                {
                  "title" : "임대조건",
                  "description" : welfare_info_house.iloc[7]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : "62870c7d75eca02fba63dd29"
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide=RH110"
                }
              ]
            },
            {
              "imageTitle": {
                "title": "공공기숙사",
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[8]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[8]['term']
                },
                {
                  "title" : "주거형태",
                  "description" : welfare_info_house.iloc[8]['dedicated_area']
                },
                {
                  "title" : "임대조건",
                  "description" : welfare_info_house.iloc[8]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : "62870c90bacfd86a3725aa26"
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide=RH111"
                }
              ]
            },
          ]
        }
      }
    ],
    "quickReplies": [
      {
        "action": "block",
        "blockId": "62873757ee5923754330c0b2",
        "label": "메인메뉴"
        
      },
      {
        "messageText": "최근 주문",
        "action": "message",
        "label": "최근 주문"
      },
      {
        "messageText": "장바구니",
        "action": "message",
        "label": "장바구니"
      }
    ]
  }
}
    
    #답변 전송
    return jsonify(res)
# --------------------------------------------------------------------------------------------------------------