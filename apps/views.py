# *-* coding=utf-8 *-*
import sys
import os

source_path = os.path.abspath(os.path.join('.'))
sys.path.append(source_path)

import json
from pprint import pprint

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import pandas as pd

from apps.models import Purchase, Products, Statistics, run_database, connect_database, logistics_search_package

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

@app.route("/save_purchase", methods=["POST"])
def save_purchase():
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
    original_data = request.get_data()
    data = json.loads(original_data)
    return Products.seed(data)

@app.route("/save_statistic", methods=["POST"])
def save_statistic():
    original_data = request.get_data()
    data = json.loads(original_data)
    return Statistics.seed(data)

@app.route("/get_statistics", methods=["POST"])
def get_statistics():
    original_data = request.get_data()
    return Statistics.get_statistics(json.loads(original_data))

@app.route("/logistics")
def logistics():
    return render_template("logistics.html")

@app.route("/get_package_info", methods=["POST"])
def get_package_info():
    original_data = request.get_data()
    return Purchase.get_package_info(json.loads(original_data))

@app.route("/search_package", methods=["POST"])
def search_package():
    original_data = request.get_data()
    return logistics_search_package(original_data.decode())
    

@app.route("/export_data", methods=["POST"])
def export_data():
    original_data = request.get_data()
    data = json.loads(original_data)
    purchase_table_data, statistic_table_data = data
    purchase_export_data = purchase_data_to_df(purchase_table_data)
    statistic_export_data = statistic_data_to_df(statistic_table_data)

    csv_name = statistic_export_data.at[1, "产品种类"] + "_" + statistic_export_data.at[1, "批次"] + ".csv"
    csv_file = os.path.join(r'/Users/W/Desktop', csv_name)
    purchase_export_data.to_csv(csv_file, header=True, index=0)
    statistic_export_data.to_csv(csv_file, mode='a', header=True, index=0)
    return "success"

def purchase_data_to_df(purchase_data):
    head, body = purchase_data
    table_content = pd.DataFrame(body)
    for index, row in table_content.iterrows():
        if index == 0:
            print(index, row["product_number"])
            continue
        elif row["product_number"] == table_content["product_number"][index-1]:
            table_content["product_number"][index] =  ""
        print(index, row["product_number"])

        
    for key in ["0", "batch_info", "product_id", "product_type", "customer_name", "package_number", "date"]:
        if key in head.keys():
            head.pop(key)
    # 调整列顺序
    sorted_table_content = table_content[list(head.keys())]
    # 替换列名
    sorted_table_content.rename(columns=head, inplace=True)
    # 更改index值，从1开始
    sorted_table_content.index = range(1,len(sorted_table_content) + 1)
    sorted_table_content.loc['__'] = ''
    pprint(sorted_table_content)
    return sorted_table_content
    
def statistic_data_to_df(statistic_data):
    head,body = statistic_data
    table_content = pd.DataFrame(body)
    print("statistics:")
    for key in ["total_cost_cn", "total_profit_eu", "total_profit_eu"]:
        if key in head.keys():
            head.pop(key)
    # 调整列顺序
    sorted_table_content = table_content[list(head.keys())]
    # 替换列名
    sorted_table_content.rename(columns=head, inplace=True)
    # 更改index值，从1开始
    sorted_table_content.index = range(1,len(sorted_table_content) + 1)
    return sorted_table_content
    

if __name__ == "__main__":
    #run_database()
    connect_database()
    app.run(app.run(host='0.0.0.0',port=5000,debug=True))