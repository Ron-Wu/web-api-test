from flask import Flask, request, redirect, url_for, render_template
import json
import pandas as pd
from pymongo import MongoClient
import ssl

app = Flask(__name__)
client = MongoClient('mongodb+srv://web:5tgbnhy6@cluster0.jwzsw.mongodb.net/API?retryWrites=true&w=majority', ssl_cert_reqs=ssl.CERT_NONE)

client_data ='''
  {
                "News": [
                    {
                        "Title": "NewsA",
                        "Tags": ["Gossiping"],
                        "Date": "2021/06/26",
                        "Detail": {
                            "Author": "Wally",
                            "Content": "Hello World"
                        }
                    },
                    {
                        "Title": "NewsB",
                        "Tags": ["Social", "Wally"],
                        "Date": "2021/06/27",
                        "Detail": {
                            "Author": "Andy",
                            "Content": "Taiwan NO.1"
                        }
                    }
                ]
            }
'''
data = json.loads(client_data)

@app.route("/")
def home():
    return "Welcome!"

@app.route("/findWally")
def FindWally():

    for i in range(len(data["News"])):
        for k, v in data["News"][i]["Detail"].items():
            if v == "Wally":
                return k

@app.route("/createNews")
def CreateNews():

    newslist = []
    for i in data["News"]:
        newslist.append(i)
        # print(i["Detail"]["Author"],i["Title"] )
        testindex = client['API']['user_info'].create_index(
            [
                ("Detail.Author", 1),
                ("Title", 1)
            ]
        )

    client['API']['user_info'].insert_many(newslist)

    return "createNews done"

@app.route('/success/<name>', methods=['GET'])
def success(name):

    filter_author={
        "Detail.Author": f"{name}"
    }

    result = list(client['API']['user_info'].find(
    filter=filter_author,
    ))

    if len(result) >= 1:
        content_list = []
        for i in range(len(result)):
            deta = result[i]['Detail']
            content_list.append(deta["Content"])
        return render_template('result.html', result = content_list)
    else:
        return ("Can't find the author!")


@app.route("/findNews", methods=['POST', 'GET'])
def FindNews():
    if request.method == 'POST':
        user = request.form['nm']

        if user != None:
            return redirect(url_for('success', name=user))

        else:
            return render_template('findNews.html')
    else:
        user = request.args.get('nm')
        if user != None:
            return redirect(url_for('success', name=user))
        else:

            return render_template('findNews.html')

if __name__=="__main__":
    app.run()
