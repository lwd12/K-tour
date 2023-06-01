from flask import Flask, render_template, request, jsonify
import requests  # pip install requests
from urllib.parse import urlencode, unquote
import json
import csv
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import sys
import urllib.request

app = Flask(__name__)  # Initialise app

load_dotenv()
client_id = os.environ.get("naver_ID")
client_secret = os.environ.get("naver_key")

filename1 = "tour_craft.csv"  # 파일 이름
filename2 = "festival.csv"
filename3 = "tourfestival2.json"
filename4 = "localfood.csv"
filename5 = "food.csv"
filename6 = "templestay.csv"
filename7 = "hanok.csv"

craft = []  # 결과를 저장할 리스트
festival = []
food = []
acc = []
with open(filename1, "r", encoding="utf-8-sig") as csvfile:  # 공방 정보
    reader = csv.DictReader(csvfile)
    for row in reader:
        data = {row["FCLTY_NM"]: [row["RDNMADR_NM"]]}
        craft.append(data)

with open(filename2, "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    for row in reader:
        data = {row["DATA_TITLE_NM"]: [row["ADDR"], row["CNTNTS_URL"]]}
        festival.append(data)

with open(filename3, "r", encoding="utf-8-sig") as f:
    data = json.load(f)
    for row in data:
        result = {row["data_title_nm"]: [row["addr"], row["cntnts_url"]]}
        festival.append(result)

with open(filename4, "r", encoding="utf-8-sig") as f:
    data = csv.DictReader(f)
    for row in data:
        result = {row["RELATE_RSTRNT_NM"]: [row["RSTRNT_ADDR"], row["CNTNTS_URL"]]}
        food.append(result)

with open(filename5, "r", encoding="utf-8-sig") as f:
    data = csv.DictReader(f)
    for row in data:
        result = {row["FCLTY_NM"]: [row["RDNMADR_NM"], row["HMPG_URL"]]}
        food.append(result)

with open(filename6, "r", encoding="utf-8-sig") as f:
    data = csv.DictReader(f)
    for row in data:
        result = {row["FCLTY_NM"]: [row["RDNMADR_NM"], row["HMPG_URL"]]}
        acc.append(result)

with open(filename7, "r", encoding="utf-8-sig") as f:
    data = csv.DictReader(f)
    for row in data:
        result = {row["FCLTY_NM"]: [row["RDNMADR_NM"], row["HMPG_URL"]]}
        acc.append(result)


def translate(data_name):
    felist = []
    fevallist = []
    feval = []
    fedat = []
    crlist = []
    crvallist = []
    crval = []
    crdat = []
    fdlist = []
    fdvallist = []
    fdval = []
    fddat = []
    acclist = []
    accvallist = []
    acval = []
    acdat = []
    alllist = []
    allvallist = []
    alval = []
    aldat = []
    for d in festival:
        for key, value in d.items():
            for i in value:
                if data_name in i:
                    felist.append(key)
                    fevallist.append(value)

    for lst in fevallist:
        feval.append(lst[0])
        fedat.append(lst[1])

    for d in craft:
        for key, value in d.items():
            for i in value:
                if data_name in i:
                    crlist.append(key)
                    crvallist.append(value)

    for lst in fevallist:
        crval.append(lst[0])
        crdat.append(lst[1])

    for d in food:
        for key, value in d.items():
            for i in value:
                if data_name in i:
                    fdlist.append(key)
                    fdvallist.append(value)

    for lst in fdvallist:
        fdval.append(lst[0])
        fddat.append(lst[1])

    for d in acc:
        for key, value in d.items():
            for i in value:
                if data_name in i:
                    acclist.append(key)
                    accvallist.append(value)

    for lst in accvallist:
        acval.append(lst[0])
        acdat.append(lst[1])

    return (
        felist,
        feval,
        fedat,
        crlist,
        crval,
        crdat,
        fdlist,
        fdval,
        fddat,
        acclist,
        acval,
        acdat,
    )


def trans(data_name):
    list = []
    vallist = []
    for d in craft:
        for key, value in d.items():
            for i in value:
                if data_name in i:
                    list.append(key)
                    vallist.append(value)

    return list, vallist


def getdata(id):
    encText = urllib.parse.quote(id)
    url = (
        "https://openapi.naver.com/v1/search/local.json?query="
        + encText
        + "&display=20&sort=comment"
    )  # JSON 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        data = json.loads(response_body)
        List = []
        address = []
        for item in data["items"]:
            title = item["title"]
            add = item["roadAddress"]
            title = title.replace("<b>", " ")
            title = title.replace("</b>", " ")
            List.append(title)

            address.append(add)

    else:
        print("Error Code:" + rescode)

    return List, address


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method != "POST":
        acd = "전통숙소"
        fdd = "전통음식"
        spd = "문화관광지"
        accom = getdata(acd)
        food = getdata(fdd)
        spot = getdata(spd)
        return render_template(
            "index.html",
            accom=accom[0],
            food=food[0],
            spot=spot[0],
            basicafd=food[1],
            basicasp=spot[1],
            basicacc=accom[1],
        )
    else:
        data_name = request.form["area"]
        print(data_name)
        result = translate(data_name)
        resultv = []
        resultk = []

        con_name = request.form["con"]
        if con_name == "숙소":
            resultv = set(result[10])
            resultv = list(resultv)
            resultk = set(result[9])
            resultk = list(resultk)
            resultk.sort()
            resultv.sort()
        elif con_name == "식당":
            resultv = set(result[7])
            resultv = list(resultv)
            resultk = set(result[6])
            resultk = list(resultk)
            resultk.sort()
            resultv.sort()

        elif con_name == "축제":
            resultv = set(result[1])
            resultv = list(resultv)
            resultk = set(result[0])
            resultk = list(resultk)
            resultk.sort()
            resultv.sort()

        elif con_name == "놀거리":
            resultv = set(result[4])
            resultv = list(resultv)
            resultk = set(result[3])
            resultk = list(resultk)
            resultk.sort()
            resultv.sort()

        return render_template(
            "search.html",
            search=resultk,
            resultv=resultv,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
