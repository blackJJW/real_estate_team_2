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

blue_house_welfare_detail_2 = Blueprint("house_welfare_detail_2", __name__, url_prefix='/house_welfare_detail_2')

@blue_house_welfare_detail_2.route("/")
def house_welfare__detail_2_home():
    return "house_welfare_detail_2"

@blue_house_welfare_detail_2.route("/move_in_target", methods=['GET', 'POST'])
def show_move_in_target():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    # ----- data url ----------------------------------------------------------------------------
    if welfare_type == '전세임대주택':
        target_data = pd.read_csv("./data/house_welfare/deposit_lease/moving_in_subject.csv")
    # -------------------------------------------------------------------------------------------
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    
    res['template']['outputs'].append({"simpleText": {"text": "■ 입주대상" + "\n\n" 
                            + '♤ ' + str(target_data.iloc[0]['class_1']) + '\n\n\t' 
                                                      + '1. ' + str(target_data.iloc[0]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[0]['description']) + '\n\n\t'
                    
                                                      + '2. ' + str(target_data.iloc[1]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[1]['description']) + '\n\n\t'
                            
                                                      + '3. ' + str(target_data.iloc[2]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[2]['description']) + '\n\n\t'
                                                      
                                                      + '4. ' + str(target_data.iloc[3]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[3]['description']) + '\n\n\t'
                                                      
                                                      + '5. ' + str(target_data.iloc[4]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[4]['description']) + '\n\n\t'
                                                      
                                                      + '6. ' + str(target_data.iloc[5]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[5]['description']) + '\n\n\t'
                            
                            + '♤ ' + str(target_data.iloc[6]['class_1']) + '\n\n\t' 
                                                      + '1. ' + str(target_data.iloc[6]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[6]['description']) + '\n\n\t'
                            + '♤ ' + str(target_data.iloc[7]['class_1']) + '\n\n\t' 
                                                      + '1. ' + str(target_data.iloc[7]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[7]['description']) + '\n\n\t'
                                                      
                                                      + '2. ' + str(target_data.iloc[8]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[8]['description']) + '\n\n\t'
                            
                            + '♤ ' + str(target_data.iloc[9]['class_1']) + '\n\n\t' 
                                                      + '1. ' + str(target_data.iloc[9]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[9]['description']) + '\n\n\t'
                                                      
                                                      + '2. ' + str(target_data.iloc[10]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[10]['description']) + '\n\n\t'
                                                      
                                                      + '3. ' + str(target_data.iloc[11]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[11]['description']) + '\n\n\t'
                                                      
                                                      + '4. ' + str(target_data.iloc[12]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[12]['description']) + '\n\n\t'
                                                      
                                                      + '5. ' + str(target_data.iloc[13]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[13]['description']) + '\n\n\t'
                                                      
                                                      + '6. ' + str(target_data.iloc[14]['class_2']) + '\n\n\t\t'
                                                      + '-- ' + str(target_data.iloc[14]['description'])
                                                     }})
    
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    if welfare_type == '전세임대주택':
        tmp_quickReplies_set['quickReplies'].append({"label": "대상주택", "action": "block", 
                                                     "blockId": "628ed39b7bd2fd433357fa84", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "전세금지원 한도액", "action": "block", 
                                                     "blockId": "628ed77b7befc3101c3bbaa0", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "임대조건", "action": "block", 
                                                     "blockId": "628eda307bd2fd433357fd25", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "임대기간", "action": "block", 
                                                     "blockId": "628edc977bd2fd433357fddb", "extra": {"welfare_type" : welfare_type}})
    
    tmp_quickReplies_set['quickReplies'].append({"label": "신청절차", "action": "block", 
                                                     "blockId": "628b38eb055a574d7df53a46", "extra": {"welfare_type" : welfare_type}})
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block", 
                                                     "blockId": "62859d5e33d26f492e9e84ed"})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block", 
                                                     "blockId": "62873757ee5923754330c0b2"})
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)

@blue_house_welfare_detail_2.route("/target_house", methods=['GET', 'POST'])
def show_target_house():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    # ----- data url ----------------------------------------------------------------------------
    if welfare_type == '전세임대주택':
        target_data = pd.read_csv("./data/house_welfare/deposit_lease/house_object.csv")
    elif welfare_type == '공공기숙사':
        target_data = pd.read_csv("./data/house_welfare/public_dormitory/recruiting_house_type.csv")
        target_data_1 = pd.read_csv("./data/house_welfare/public_dormitory/dwelling_type.csv")
    else:
        pass
    # -------------------------------------------------------------------------------------------
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    
    if welfare_type == '전세임대주택':
        res['template']['outputs'].append({"simpleText": {"text": "■ 대상주택" + "\n\n\t" 
                                                      + "♤ " + target_data.iloc[0]['object'] + '\n\t' 
                                                          + target_data.iloc[0]['note']
                                                      }})
        
    elif welfare_type == '공공기숙사':
        res['template']['outputs'].append({"simpleText": {"text": "■ 주택유형" + "\n\n\t" 
                                                      + "♤ " + target_data.iloc[0]['class'] + '\n\t' 
                                                          + "* " + target_data.iloc[0]['type'] + '\n\t\t'
                                                              + "- " + target_data.iloc[0]['room'] + '\n\t\t'
                                                              + "- " + target_data.iloc[1]['room'] + '\n\t\t'
                                                              + "- " + target_data.iloc[2]['room'] + '\n\n'
                                                      + "♤ " + target_data.iloc[3]['class'] + '\n\t' 
                                                          + "* " + target_data.iloc[3]['type'] + '\n\t\t'
                                                              + "- " + target_data.iloc[3]['room'] + '\n\t\t'
                                                              + "- " + target_data.iloc[4]['room'] + '\n\t\t'
                                                              + "- " + target_data.iloc[5]['room']
                                                      }})
        res['template']['outputs'].append({"simpleText": {"text": "■ 주거형태" + "\n\n\t" 
                                                      + "♤ " + target_data_1.iloc[0]['type'] + '\n\t' 
                                                          + target_data_1.iloc[0]['note'] + '\n\n'
                                                      + "♤ " + target_data_1.iloc[1]['type'] + '\n\t' 
                                                          + target_data_1.iloc[1]['note'] + '\n\n'
                                                      + "♤ " + target_data_1.iloc[2]['type'] + '\n\t' 
                                                          + target_data_1.iloc[2]['note'] 
                                                      }})
    else:
        pass
    
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    if welfare_type == '전세임대주택':
        tmp_quickReplies_set['quickReplies'].append({"label": "입주대상", "action": "block", 
                                                     "blockId": "628ddcbb7bd2fd433357f026", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "전세금지원 한도액", "action": "block", 
                                                     "blockId": "628ed77b7befc3101c3bbaa0", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "임대조건", "action": "block", 
                                                     "blockId": "628eda307bd2fd433357fd25", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "임대기간", "action": "block", 
                                                     "blockId": "628edc977bd2fd433357fddb", "extra": {"welfare_type" : welfare_type}})
    
    tmp_quickReplies_set['quickReplies'].append({"label": "신청절차", "action": "block", 
                                                     "blockId": "628b38eb055a574d7df53a46", "extra": {"welfare_type" : welfare_type}})
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block", 
                                                     "blockId": "62859d5e33d26f492e9e84ed"})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block", 
                                                     "blockId": "62873757ee5923754330c0b2"})
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)


@blue_house_welfare_detail_2.route("/support_limit", methods=['GET', 'POST'])
def show_support_limit():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    # ----- data url ----------------------------------------------------------------------------
    if welfare_type == '전세임대주택':
        limit_data = pd.read_csv("./data/house_welfare/deposit_lease/deposit_support_limit.csv")
    # -------------------------------------------------------------------------------------------
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    
    res['template']['outputs'].append({"simpleText": {"text": "■ 전세지원 한도액" + "\n\n\t" 
                                                      + "♤ " + limit_data.iloc[0]['money'] + '\n\n\t' 
                                                          + limit_data.iloc[0]['note']
                                                      }})
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    if welfare_type == '전세임대주택':
        tmp_quickReplies_set['quickReplies'].append({"label": "입주대상", "action": "block", 
                                                     "blockId": "628ddcbb7bd2fd433357f026", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "대상주택", "action": "block", 
                                                     "blockId": "628ed39b7bd2fd433357fa84", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "임대조건", "action": "block", 
                                                     "blockId": "628eda307bd2fd433357fd25", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "임대기간", "action": "block", 
                                                     "blockId": "628edc977bd2fd433357fddb", "extra": {"welfare_type" : welfare_type}})
    
    tmp_quickReplies_set['quickReplies'].append({"label": "신청절차", "action": "block", 
                                                     "blockId": "628b38eb055a574d7df53a46", "extra": {"welfare_type" : welfare_type}})
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block", 
                                                     "blockId": "62859d5e33d26f492e9e84ed"})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block", 
                                                     "blockId": "62873757ee5923754330c0b2"})
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)

@blue_house_welfare_detail_2.route("/lease_condition", methods=['GET', 'POST'])
def show_lease_condition():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    # ----- data url ----------------------------------------------------------------------------
    if welfare_type == '전세임대주택':
        condition_data = pd.read_csv("./data/house_welfare/deposit_lease/lease_condition.csv")
    # -------------------------------------------------------------------------------------------
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    
    res['template']['outputs'].append({"simpleText": {"text": "■ 임대조건" + "\n\n\t" 
                                                      + "♤ " + condition_data.iloc[0]['condition'] + '\n\t' 
                                                          + condition_data.iloc[0]['description'] + '\n\n' 
              
                                                      + "♤ " + condition_data.iloc[1]['condition'] + '\n\t' 
                                                          + condition_data.iloc[1]['description'] + '\n\n\t' 
                                                          + condition_data.iloc[1]['note']
                                                      }})
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    if welfare_type == '전세임대주택':
        tmp_quickReplies_set['quickReplies'].append({"label": "입주대상", "action": "block", 
                                                     "blockId": "628ddcbb7bd2fd433357f026", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "대상주택", "action": "block", 
                                                     "blockId": "628ed39b7bd2fd433357fa84", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "전세금지원 한도액", "action": "block", 
                                                     "blockId": "628ed77b7befc3101c3bbaa0", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "임대기간", "action": "block", 
                                                     "blockId": "628edc977bd2fd433357fddb", "extra": {"welfare_type" : welfare_type}})
    
    tmp_quickReplies_set['quickReplies'].append({"label": "신청절차", "action": "block", 
                                                     "blockId": "628b38eb055a574d7df53a46", "extra": {"welfare_type" : welfare_type}})
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block", 
                                                     "blockId": "62859d5e33d26f492e9e84ed"})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block", 
                                                     "blockId": "62873757ee5923754330c0b2"})
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)

@blue_house_welfare_detail_2.route("/lease_term", methods=['GET', 'POST'])
def show_lease_term():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    # ----- data url ----------------------------------------------------------------------------
    if welfare_type == '전세임대주택':
        term_data = pd.read_csv("./data/house_welfare/deposit_lease/lease_term.csv")
    # -------------------------------------------------------------------------------------------
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    
    res['template']['outputs'].append({"simpleText": {"text": "■ 임대기간" + "\n\n\t" 
                                                      + "♤ " + term_data.iloc[0]['term'] + '\n\n\t' 
                                                          + term_data.iloc[0]['note']
                                                      }})
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    if welfare_type == '전세임대주택':
        tmp_quickReplies_set['quickReplies'].append({"label": "입주대상", "action": "block", 
                                                     "blockId": "628ddcbb7bd2fd433357f026", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "대상주택", "action": "block", 
                                                     "blockId": "628ed39b7bd2fd433357fa84", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "전세금지원 한도액", "action": "block", 
                                                     "blockId": "628ed77b7befc3101c3bbaa0", "extra": {"welfare_type" : welfare_type}})
        tmp_quickReplies_set['quickReplies'].append({"label": "임대조건", "action": "block", 
                                                     "blockId": "628eda307bd2fd433357fd25", "extra": {"welfare_type" : welfare_type}})
    
    tmp_quickReplies_set['quickReplies'].append({"label": "신청절차", "action": "block", 
                                                     "blockId": "628b38eb055a574d7df53a46", "extra": {"welfare_type" : welfare_type}})
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block", 
                                                     "blockId": "62859d5e33d26f492e9e84ed"})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block", 
                                                     "blockId": "62873757ee5923754330c0b2"})
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)