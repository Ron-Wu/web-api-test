from flask import Flask
import mongoengine as db
from pymongo import MongoClient
import json
from flask_mongoengine import MongoEngine
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

@app.route("/findWally")
def FindWally():
    for i in range(len(data["News"])):
        for k, v in data["News"][i]["Detail"].items():
            if v == "Wally":
                return k

@app.route("/createNews")
def CreateNews():

    database_name = "test-db-ron"
    database_uri = f"mongodb+srv://cluster0.jwzsw.mongodb.net/{database_name}?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"

    # 通過MONGODB_SETTINGS配置MongoEngine
    app.config["MONGODB_SETTINGS"] = {
        'db': 'test-db-ron',
        # 'host': database_uri,
        # 'port': 27017,
        # 'connect': True,
        # 'username': 'f10604r',
        # 'password': 'ron10604',
        # 'authentication_source': 'admin'
    }

    import mongoengine as me

    class user_infos(me.Document):
        Title = me.StringField()
        Tags = me.StringField()
        Date = me.DateField()
        Detail = me.DictField()

    # 初始化 MongoEngine
    db = MongoEngine(app)
    # db.user_info.insert(data)

    data = [{
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
            }]




    newsa ={
            "Title": "NewsA",
            "Tags": ["Gossiping"],
            "Date": "2021/06/26",
            "Detail": {
                "Author": "Wally",
                "Content": "Hello World"
            }}

    # filter = {
    #     123 : '456'
    # }
    # maxTimeMS = 1
    #
    # result = client['test-db-ron']['user_info'].find(
    #     filter=filter,
    #     max_time_ms=maxTimeMS
    # )
    # df = pd.Series(result)
    # ds = df[0]
    # print(ds)
    # db.user_info.insert(newsa)

    # result = client["test-db-ron"]['user_info'].insert(data)
    db["user_infos"].insert(newsa)

    print("done")
    return "done"

@app.route("/findNews")
def FindNews():
    return "findNews"

if __name__=="__main__":
    app.run(host='0.0.0.0')
