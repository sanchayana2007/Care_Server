from flask import Flask,render_template
from rest_api  import get_call,post_call,put_call
import json
app = Flask(__name__)


@app.route("/")
def home():
  api = 'booking/slotadd'
  body= {'aid' : 1,'did' : '608bc4507b40eb6803659557','cid' : '608793ae5c88f3bdb38d6530','date': '17/05/2021'}
  t= get_call(api,body)
  if t:
    return render_template("home.html", data=t["result"][0])
  else:
    return render_template("home.html")
    
@app.route("/John")
def John():
  return "Hello John."

@app.route("/about")
def about():
  return render_template("about.html")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port= 4444, debug=True)
