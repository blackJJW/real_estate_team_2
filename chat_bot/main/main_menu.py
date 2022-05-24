from flask import Blueprint
from flask import Flask, request, jsonify

blue_main_menu = Blueprint("main_menu", __name__, url_prefix="/main_menu")

@blue_main_menu.route("/")
def main_menu_check():
    return "main_menu"

@blue_main_menu.route("/main", methods=['GET', 'POST'])
def main_menu_1():
    body = request.get_json()
    
    res = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "basicCard": {
          "title": "메인메뉴",
          "description": "원하는 메뉴를 선택해주세요.",
          "thumbnail": {
            "imageUrl": ""
          },
          "profile": {
            "imageUrl": "",
            "nickname": "메인메뉴"
          },
          "buttons": [
            {
              "label": "주택복지",
              "action": "block",
              "blockId": "62859d5e33d26f492e9e84ed"
            }
            
          ]
        }
      }
    ]
  }
}
    return res