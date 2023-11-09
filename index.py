import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


from flask import Flask, render_template,request

from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():

	homepage = "<h1>梅祐銘Python網頁<br>2023/11/9</h1>"

	homepage += "<a href=/mis>MIS</a><br>"

	homepage += "<a href=/today>顯示日期時間</a><br>"

	homepage += "<a href=/welcome?nick=tcyang>傳送使用者暱稱</a><br>"

	homepage += "<a href=/about>子青簡介網頁</a><br>"

	homepage +=  "<a href=/account>網頁表單</a>"

	homepage += "</br><a href=/wave>演員名單(年齡由小到大)</a>"

	return homepage



@app.route("/mis")

def course():

	return "<h1>資訊管理導論</h1>"

@app.route("/today")

def today():

	now = datetime.now()

	return render_template("today.html", datetime = str(now))


@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")


@app.route("/welcome", methods=["GET", "POST"])
def welcome():

		user = request.values.get("nick")

		return render_template("welcome.html", name=user)

@app.route("/wave")
def read():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("人選之人─造浪者")    
    docs = collection_ref.order_by("birth", direction=firestore.Query.DESCENDING).get()    
    for doc in docs:         
        Result += "演員：{}".format(doc.to_dict()) + "<br>"    
    return Result


		
#if __name__ == "__main__":
#	app.run()