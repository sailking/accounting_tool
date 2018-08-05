# *-* coding=utf-8 *-*
import json
from pprint import pprint

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from app.models import Purchase, Products, connect_database

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_product_list", methods=["POST"])
def get_product_type_list():
    return Products.get_product_type_list()

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
def save_date_form_table():
    if request.method == "POST":
        print("method is post")
        original_data = request.get_data()   #从post请求中获得原始json数据
        data = json.loads(original_data)
    return Purchase.seed(data)

@app.route("/getbatch", methods=["POST"])
def get_batch():
    original_data = request.get_data()
    return Purchase.get_batch(original_data.decode())

if __name__ == "__main__":
    connect_database()
    app.run(debug=True)
    
    
