from flask import flask, request
app = flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        'text': "안녕 hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody

# 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    print(body)
    print(bodt['userRequest']['utterance'])

    responseBody = {
        "version": "2.0"
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                       "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                       "altText": "hello I'm Ryan"
                    }
                }
            ]
        }
    }
    return responseBody
