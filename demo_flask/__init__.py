from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import socket
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
app = Flask(__name__)
#run_with_ngrok(app)


def get_ara_object(pgm_id):
    with requests.Session() as ss:
        ara_login_data = {"userId": "swing", "userPwd": "sktarA12~!"}
        ara_login_url = "http://sara.sktelecom.com:8080/araws/loginSvc/Login"
        ara_login_r = ss.post(ara_login_url,data=ara_login_data)
        pgm_info_url = 'http://sara.sktelecom.com:8080/araws/objectSvc/Search/ListNm?dmnCd=SKT&prjCd=SWING&oprCd=SWGS&objId={}&posStart=0&posEnd=42'.format(pgm_id)
        pgm_info_r = ss.get(pgm_info_url)
        result_json = json.loads(pgm_info_r.text)
        print(result_json['items'][0]['objNm'],result_json['items'][0]['crgrId'])
        return result_json['items'][0]['objNm'], result_json['items'][0]['crgrId']


@app.route("/")
def index():
    return "Hello world"

@app.route("/getProgram",methods=['GET'])
def getProgram():
    a, b = get_ara_object("ordss00tst01t01.c")
    print(a,b)
    return "Good"

@app.route("/postProgram",methods=['POST'])
def postProgram():
    req = request.get_json()
    pgm_id = req["action"]["detailParams"]["pgm_id"]["value"]
    pgm_des,name = get_ara_object(pgm_id)
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "프로그램 ID : " + pgm_id+"\n"+
                                "프로그램 Name : " + pgm_des+"\n"+
                                "프로그램 담당자 : " + name
                    }
                }
            ]
        }
    }
    return jsonify(res)