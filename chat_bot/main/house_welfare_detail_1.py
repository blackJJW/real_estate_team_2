from flask import Blueprint
from flask import Flask, request, jsonify
import pandas as pd
import json

# ------------------------------------------------------------------------------------------------------
service_code = {'통합공공임대주택' : 'RH112', '영구임대주택' : 'RH103', '국민임대주택' : 'RH104',
                '장기전세주택' : 'RH105', '공공임대주택' : 'RH106', '전세임대주택' : 'RH107',
                '행복주택' : 'RH108', '공공지원민간임대주택' : 'RH109', '주거복지동주택' : 'RH110',
                '공공기숙사' : 'RH111'}

URL = "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide="
# ------------------------------------------------------------------------------------------------------

blue_house_welfare_detail_1 = Blueprint("house_welfare_detail_1", __name__, url_prefix='/house_welfare_detail_1')

@blue_house_welfare_detail_1.route("/")
def house_welfare__detail_1_home():
    return "house_welfare_detail_1"

# ----- selection_criteria ------------------------------------------------------------------------------------------------------
@blue_house_welfare_detail_1.route("/selection_criteria", methods=['GET', 'POST'])
def show_selection_criteria():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    
    if welfare_type == '국민임대주택':
        res['template']['outputs'].append({"simpleText": {"text": "■ 일반공급 대상자 입주자 선정기준"}})
        res['template']['outputs'].append({"basicCard": {
                    "title": "전용면적 50㎡ 미만인 주택",
                    "thumbnail": {"imageUrl": "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/id01_1.jpg",
                                 "link":{"web" : "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/id01_1.jpg"}}}})
        res['template']['outputs'].append({"basicCard": {
                    "title": "전용면적 50㎡ 이상인 주택",
                    "thumbnail": {"imageUrl": "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/id01_2.jpg",
                                 "link":{"web" : "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/id01_2.jpg"}}}})
    
    tmp_quickReplies_set['quickReplies'].append({"label": "입주자격", "action": "block", 
                                                     "blockId": "628b0241bacfd86a3725d282", "extra": {"welfare_type" : welfare_type}})
    
    if welfare_type == '국민임대주택':
        tmp_quickReplies_set['quickReplies'].append({"label": "소득·자산 산정방법", "action": "block", 
                                                     "blockId": "628b1ed4055a574d7df534ff", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "일반공급 자격·선정순위", "action": "block", 
                                                     "blockId": "628b2f71055a574d7df5383d", "extra": {"welfare_type" : welfare_type}})
    else:
        pass

        
    tmp_quickReplies_set['quickReplies'].append({"label": "신청절차", "action": "block", 
                                                     "blockId": "628b38eb055a574d7df53a46", "extra": {"welfare_type" : welfare_type}})
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block", 
                                                     "blockId": "62859d5e33d26f492e9e84ed"})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block", 
                                                     "blockId": "62873757ee5923754330c0b2"})
    
    res['template'].update(tmp_quickReplies_set)
    
    
    return jsonify(res)
# ------------------------------------------------------------------------------------------------------------------------------------------


@blue_house_welfare_detail_1.route("/lease_money_level", methods=['GET', 'POST'])
def lease_money_level():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    
    if welfare_type == '장기전세주택':
        res['template']['outputs'].append({"simpleText": {"text": "■ 임대보증금 수준" + "\n\n\t" 
                                                          + "장기전세주택으로 공급하는 공공건설임대주택과 같거나 인접한 시·군·구에 있는 주택 중 해당 임대주택과 유형, 규모, 생활여건 등이 비슷한 2개또는 3개 단지의 공동주택의 전세계약금액을 평균한 금액의 80%"
                                                         }})
    
    
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    
    tmp_quickReplies_set['quickReplies'].append({"label": "입주자격", "action": "block", 
                                                     "blockId": "628b0241bacfd86a3725d282", "extra": {"welfare_type" : welfare_type}})
    
    
    if welfare_type != '장기전세주택':
        tmp_quickReplies_set['quickReplies'].append({"label": "신청절차", "action": "block",
                                                     "blockId": "628b38eb055a574d7df53a46", "extra": {"welfare_type" : welfare_type}})
    else:
        pass
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block",
                                                     "blockId": "62859d5e33d26f492e9e84ed"})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block",
                                                     "blockId": "62873757ee5923754330c0b2"})
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)


@blue_house_welfare_detail_1.route("/house_type", methods=['GET', 'POST'])
def show_house_type():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    # ----- data url ---------------------------------------------------------------------
    if welfare_type == '공공임대주택':
        house_data = pd.read_csv("./data/house_welfare/public_lease/housing_type.csv")
    # ------------------------------------------------------------------------------------
    
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    
    res['template']['outputs'].append({"simpleText": {"text": "■ 주택유형" + "\n\n\t" 
                                                          + "♤ " + house_data.iloc[0]['type'] + ': ' + '\n\n\t' 
                                                      + "- " + house_data.iloc[0]['description'] + '\n\n\n'
                                                      + "♤ " + house_data.iloc[1]['type'] + ': ' + '\n\n\t' 
                                                      + "- " + house_data.iloc[1]['description']}})
    
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    if welfare_type == '공공임대주택':
        tmp_quickReplies_set['quickReplies'].append({"label": "입주자 선정순위", "action": "block", 
                                                     "blockId": "628b412f299dbd02ee7a6666", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "특별공급", "action": "block", 
                                                     "blockId": "628dcfa251c40d32c6d8a42e", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "분양전환", "action": "block", 
                                                     "blockId": "628dd5c77befc3101c3bad00", "extra": {"welfare_type" : welfare_type}})
    
    tmp_quickReplies_set['quickReplies'].append({"label": "신청절차", "action": "block", 
                                                     "blockId": "628b38eb055a574d7df53a46", "extra": {"welfare_type" : welfare_type}})
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block",
                                                     "blockId": "62859d5e33d26f492e9e84ed"})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block",
                                                     "blockId": "62873757ee5923754330c0b2"})
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)


@blue_house_welfare_detail_1.route("/special_supply", methods=['GET', 'POST'])
def show_special_supply():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    # ----- data url ---------------------------------------------------------------------
    if welfare_type == '공공임대주택':
        supply_data = pd.read_csv("./data/house_welfare/public_lease/special_supply.csv")
    # ------------------------------------------------------------------------------------
    
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    
    res['template']['outputs'].append({"simpleText": {"text": "■ 특별공급" + "\n\n\t" 
                                                      + "♤ " + supply_data.iloc[0]['class'] + ': ' + '\n\n\t' 
                                                      + "- 비율 : " + supply_data.iloc[0]['ratio'] + '\n\n\t'
                                                      + "- 입주자격 \n: " + supply_data.iloc[0]['qual'] + '\n\n\n'
                                                      + "♤ " + supply_data.iloc[1]['class'] + ': ' + '\n\n\t' 
                                                      + "- 비율 : " + supply_data.iloc[1]['ratio'] + '\n\n\t'
                                                      + "- 입주자격 \n: " + supply_data.iloc[1]['qual'] + '\n\n\n'
                                                      + "♤ " + supply_data.iloc[2]['class'] + ': ' + '\n\n\t' 
                                                      + "- 비율 : " + supply_data.iloc[2]['ratio'] + '\n\n\t'
                                                      + "- 입주자격 : \n" + supply_data.iloc[2]['qual'] + '\n\n\n'
                                                      + "♤ " + supply_data.iloc[3]['class'] + ': ' + '\n\n\t' 
                                                      + "- 비율 : " + supply_data.iloc[3]['ratio'] + '\n\n\t'
                                                      + "- 입주자격 : \n" + supply_data.iloc[3]['qual'] + '\n\n\n'
                                                      + "♤ " + supply_data.iloc[4]['class'] + ': ' + '\n\n\t' 
                                                      + "- 비율 : " + supply_data.iloc[4]['ratio'] + '\n\n\t'
                                                      + "- 입주자격 : \n" + supply_data.iloc[4]['qual'] + '\n\n\n'
                                                      + "♤ " + supply_data.iloc[5]['class'] + ': ' + '\n\n\t' 
                                                      + "- 비율 : " + supply_data.iloc[5]['ratio'] + '\n\n\t'
                                                      + "- 입주자격 : \n" + supply_data.iloc[5]['qual']
                                                     }})
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    if welfare_type == '공공임대주택':
        tmp_quickReplies_set['quickReplies'].append({"label": "주택유형", "action": "block", 
                                                     "blockId": "628dc63d43b3015cb0df8a2c", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "입주자 선정순위", "action": "block", 
                                                     "blockId": "628b412f299dbd02ee7a6666", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "분양전환", "action": "block", 
                                                     "blockId": "628dd5c77befc3101c3bad00", "extra": {"welfare_type" : welfare_type}})
    
    tmp_quickReplies_set['quickReplies'].append({"label": "신청절차", "action": "block", 
                                                     "blockId": "628b38eb055a574d7df53a46", "extra": {"welfare_type" : welfare_type}})
    
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block",
                                                     "blockId": "62859d5e33d26f492e9e84ed"})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block",
                                                     "blockId": "62873757ee5923754330c0b2"})
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)

@blue_house_welfare_detail_1.route("/sales_conversion", methods=['GET', 'POST'])
def show_sales_conversion():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    
    if welfare_type == '공공임대주택':
        res['template']['outputs'].append({"simpleText": {"text": "■ 분양전환(5년/10년 공공임대주택)" + "\n\n\t" 
                                                      + "♤ " + "분양전환 대상자" + '\n\n\t' 
                                                          + "- " + "전용 85㎡ 이하 \n\t\t 입주일 이후부터 분양전환 당시까지 해당 주택에 거주한 무주택자인 임차인" + '\n\n'
                                                          + "- " + "전용 85㎡ 초과 \n\t\t 분양전환 당시 거주하고 있는 임차인" + '\n\n'
                                                      + "♤ " + "분양전환 시기" + '\n\n\t'
                                                          + "- " + "임대의무기간(5년, 10년) 종료 후" + '\n\n'
                                                      + "♤ " + "분양전환 가격" + '\n\n\t'
                                                          + "- " + "5년 임대주택 : (건설원가+감정가격)/2" + '\n\n'
                                                          + "- " + "10년 임대주택 : 감정가격" + '\n\n'
                                                      }})
    
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    if welfare_type == '공공임대주택':
        tmp_quickReplies_set['quickReplies'].append({"label": "주택유형", "action": "block", 
                                                     "blockId": "628dc63d43b3015cb0df8a2c", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "입주자 선정순위", "action": "block", 
                                                     "blockId": "628b412f299dbd02ee7a6666", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "특별공급", "action": "block", 
                                                     "blockId": "628dcfa251c40d32c6d8a42e", "extra": {"welfare_type" : welfare_type}})
    
    tmp_quickReplies_set['quickReplies'].append({"label": "신청절차", "action": "block", 
                                                     "blockId": "628b38eb055a574d7df53a46", "extra": {"welfare_type" : welfare_type}})
    
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block",
                                                     "blockId": "62859d5e33d26f492e9e84ed"})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block",
                                                     "blockId": "62873757ee5923754330c0b2"})
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)