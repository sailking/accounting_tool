# *-* coding=utf-8 *-*

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from pprint import pprint
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/logistics")
def logistics():
    return render_template("logistics.html") 

@app.route("/tables")
def tables():
    return render_template("table.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/datafromtable", methods=['GET','POST'])
def datafromtable():
    if request.method == "POST":
        print("method is post")
        data = request.get_data()   #从post请求中获得原始json数据
        dict = json.loads(data)[0]    #将json数据转换成python数据格式
        print(dict)
    return "success"

if __name__ == "__main__":
    app.run(debug=True)
