# *-* coding=utf-8 *-*
import json
from pprint import pprint

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from app.models import Purchase, Products, connect_database

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_batch_list", methods=["POST"])
def get_batch_lset():
    original_data = request.get_data()
    return Purchase.get_batch_list(original_data.decode())

@app.route("/get_purchase", methods=["POST"])
def get_purchase():
    original_data = request.get_data()
    return Purchase.get_purchase(json.loads(original_data))

@app.route("/purchase_save", methods=["POST"])
def purchase_save():
    original_data = request.get_data()
    data = json.loads(original_data)
    return Purchase.seed(data)

@app.route("/purchase_delete", methods=["POST"])
def purchase_delete():
    original_data = request.get_data()
    return Purchase.purchase_delete(json.loads(original_data))

@app.route("/get_product_names", methods=["POST"])
def get_product_names():
    original_data = request.get_data()
    return Products.get_product_names(original_data.decode())

@app.route("/get_product", methods=["POST"])
def get_product():
    original_data = request.get_data()
    return Products.get_product(original_data.decode())

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/get_type_list", methods=["POST"])
def get_type_list():
    return Products.get_product_type_list()

@app.route("/get_product_list", methods=["POST"])
def get_product_list():
    original_data = request.get_data()
    return Products.get_product_list(original_data.decode())

@app.route("/products_delete", methods=["POST"])
def products_delete():
    original_data = request.get_data()
    data = json.loads(original_data)
    return Products.products_delete(data)

@app.route("/products_save", methods=["POST"])
def products_save():
    original_data = request.get_data()   #从post请求中获得原始json数据
    data = json.loads(original_data)
    return Products.seed(data)

@app.route("/logistics")
def logistics():
    return render_template("logistics.html") 

@app.route("/tables")
def tables():
    return render_template("table.html")

@app.route("/base")
def test():
    return render_template("base.html")

if __name__ == "__main__":
    connect_database()
    app.run(debug=True)
    
    
