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
def house_welfare__detail_1_home():
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
                                                      + '-- ' + str(target_data.iloc[14]['description']) + '\n\n\t'
                            }})
    
    return jsonify(res)