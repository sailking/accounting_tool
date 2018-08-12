# *-* coding=utf-8 *-*

import os
import sys
from datetime import datetime
from pprint import pprint
import configparser
import json
import requests

import pymongo 
import mongoengine
from mongoengine.document import DynamicDocument
from mongoengine.fields import StringField, IntField, FloatField, DateTimeField, ListField, ReferenceField
from pymongo.errors import ServerSelectionTimeoutError
from ipywidgets.widgets.widget_float import FloatSlider


def run_database():
    status = os.system('sh /Users/W/Desktop/master.sh')
    print("status: {}".format(status))

def connect_database():
        cf = configparser.ConfigParser()
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.cfg")
        print(config_file_path)
        cf.read(config_file_path)
        db = mongoengine.connect(db = cf.get("Database", "db"),
                                 host = cf.get("Database", "host"),
                                 serverSelectionTimeoutMS=120)
        try:
            info = db.server_info() # Forces a call.
        except ServerSelectionTimeoutError:
            print("server is down.")
            os._exit(0)
            
def logistics_search_package(package_number):
    try:
        com_autoauth_url = "https://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text={}".format(package_number)
        response_data = json.loads(requests.get(com_autoauth_url).text)
        com_name = response_data["auto"][0]["comCode"]
        search_url = "https://www.kuaidi100.com/query?type={}&postid={}".format(com_name, package_number)
        package_info = json.loads(requests.get(search_url).text)
        json_info = json.dumps(package_info)
    except Exception as e:
        return e
    else:
        return json_info

def str_to_float(data=None):
    print("data: {}".format(data))
    if data == None or data == "NaN":
        result = 0
    else:
        result = float(data)
    return result
           
class Customer(DynamicDocument):
    customer_number = IntField(unique=True)
    customer_name = StringField()
    customer_id = StringField()
    customer_name_address = StringField()
    
    @classmethod
    def seed(cls, data):
        pass
    
    @classmethod
    def get_customer_list(cls):
        pass      
                   
class Purchase(DynamicDocument):
    product_id = IntField()
    product_number = IntField()
    product_name = StringField()
    product_count = IntField()
    single_original_price = FloatField()
    discount = FloatField()
    single_buy_price = FloatField()
    total_buy_price = FloatField()
    single_sell_price = FloatField()
    total_sell_price = FloatField()
    single_profit = FloatField()
    total_profit = FloatField()
    date = StringField()
    packaging = StringField()
    product_type = StringField()
    batch_info = StringField()
    customer_name = StringField()
    package_number = StringField()
    
    @classmethod
    def seed(cls, data):
        print("call purchase save")
        try:
            mode, purchase_data = data
            print("mode: {}".format(mode))
            print("purchase_data: ")
            pprint(purchase_data)
            if not purchase_data:
                return "None"
            for purchase in purchase_data:
                if purchase["batch_info"] == "未设置":
                    return "批次未标明，请核对后重新保存"
                if purchase["single_sell_price"] =="" and mode == "对账模式":
                    return "售价未标明，请核对后重新保存"
            
            for purchase in purchase_data:    
                item = Purchase.objects(product_number=purchase["product_number"], discount=purchase["discount"], batch_info=purchase["batch_info"], product_type=purchase["product_type"]).first()
                if item is None:
                    print("create new")
                    item = Purchase()
                
                item.product_number = purchase["product_number"]
                item.product_type = purchase["product_type"]
                item.product_name = purchase["product_name"]
                item.product_count = int(purchase["product_count"])
                item.single_original_price = str_to_float(purchase["single_original_price"])
                item.discount = float(purchase["discount"])
                item.single_buy_price = str_to_float(purchase["single_buy_price"])
                item.total_buy_price = str_to_float(purchase["total_buy_price"])
                item.single_sell_price = str_to_float(purchase["single_sell_price"])
                item.total_sell_price = str_to_float(purchase["total_sell_price"])
                item.single_profit = str_to_float(purchase["single_profit"])
                item.total_profit = str_to_float(purchase["total_profit"])
                item.packaging = purchase["packaging"]
                item.customer_name = purchase["customer_name"]
                item.package_number = purchase["package_number"]
                item.date = purchase["date"]
                item.batch_info = purchase["batch_info"]
                   
                item.save()
                
            return "货品保存成功"
        except Exception as e:
            print("错误信息：{}".format(e))
            return "保存货品过程中出现错误"
    
    @classmethod
    def get_batch_list(cls, type_name):
        batch_list = Purchase.objects(product_type=type_name).distinct(field="batch_info")
        print(batch_list)
        return json.dumps(batch_list)
        
    @classmethod
    def get_purchase(cls, info):
        product_type, batch_info = info
        products = Purchase.objects(product_type=product_type, batch_info=batch_info)
        json_data = products.to_json()
        return json_data
    
    @classmethod
    def purchase_delete(cls, info):
        product_id, product_type, batch_info = info
        try:
            item = Purchase.objects(product_id=product_id, product_type=product_type, batch_info=batch_info).first()
            if item:
                item.delete()
                return "{}->{}->{}".format(product_type, batch_info, product_id)
            else:
                print("没有此项")
                return ""
        except Exception as e:
            print(e)
            return e
    
    @classmethod
    def get_package_info(cls, info):
        product_type, batch_info = info, batch_info = info
        json_data = []
        customer_list = Purchase.objects(product_type=product_type, batch_info=batch_info).distinct(field="customer_name")
        print(customer_list)
        for customer_name in customer_list:
            package_data = {}
            purchase_list = Purchase.objects(customer_name=customer_name)
            buy_list = ""
            for purchase in purchase_list:
                package_data["customer_name"] = purchase.customer_name
                if purchase.package_number != "0":
                    package_data["package_number"] = purchase.package_number
                purchase_info = "{}*{} \t".format(purchase.product_name, purchase.product_count)
                buy_list = buy_list + purchase_info
            package_data["buy_list"] = buy_list
            json_data.append(package_data)
        json_data = json.dumps(json_data)
        return json_data
  
class Products(DynamicDocument):
    product_id = IntField()
    product_name = StringField(unique=True)
    single_original_price = FloatField()
    discount = FloatField()
    product_count = IntField()
    exchange_rate = FloatField()
    product_type = StringField()
    
    @classmethod
    def get_product_type_list(cls):
        product_types = Products.objects.distinct(field="product_type")
        return json.dumps(product_types)
    
    @classmethod
    def get_product_list(cls, product_type):
        product_list = Products.objects(product_type=product_type)
        json_data = product_list.to_json()
        return json_data
    
    @classmethod
    def get_product_names(cls, product_type):
        """首页
                        添加产品后，点击修改产品名称，此时从products collection中读取该产品类型中的所有产品名称
        """
        product_names_list = Products.objects(product_type=product_type).distinct(field="product_name")
        product_names_list.sort()
        return json.dumps(product_names_list)
    
    @classmethod
    def get_product(cls, product_name):
        print(product_name)
        product = Products.objects(product_name=product_name).first()
        json_data = product.to_json()
        return json_data
    
    @classmethod
    def products_delete(cls, product_names):
        try:
            delete_list = []
            for product_name in product_names:
                print(product_names)
                item = Products.objects(product_name=product_name).first()
                delete_list.append(item.product_name)
                if item:
                    item.delete()
            return "删除成功"
        except Exception as e:
            print(e)
            return e
        
    @classmethod
    def seed(cls, data):
        print("call products seed")
        try:
            for product in data:
                print(product)
                item = Products.objects(product_name=product["product_name"]).first()
                if item is None:
                    print("create new product")
                    item = Products()
                    
                item.product_type = product["product_type"]
                item.product_name = product["product_name"]
                item.single_original_price = float(product["single_original_price"])
                item.discount = float(product["discount"])

                item.save()
            return "产品信息保存成功"
        except Exception as e:
            print(e)
            return e
        
class Statistics(DynamicDocument):
    product_type = StringField()
    batch_info = StringField()
    postage = FloatField()
    packaging_fee = FloatField()
    
    @classmethod
    def seed(cls, data):
        print("call statistic save")
        try:
            mode, statistic_data = data
            print("statistic_data: {}".format(statistic_data))
            if not statistic_data:
                return "None"
            for batch in statistic_data:
                pprint(batch)
                item = Statistics.objects(product_type=batch["product_type"], batch_info=batch["batch_info"]).first()
                if item is None:
                    print("create new Statistics")
                    item = Statistics()
                item.product_type = batch["product_type"]
                item.batch_info = batch["batch_info"]
                if batch["packaging_fee"] == "":
                    batch["packaging_fee"] = 0
                item.packaging_fee = float(batch["packaging_fee"])
                if batch["postage"] == "":
                    batch["postage"] = 0
                item.postage = float(batch["postage"])

                item.save()
            return "统计信息保存成功"
        except Exception as e:
            print(e)
            return "保存统计信息时出现错误"
        
    @classmethod
    def get_statistics(cls, info):
        product_type, batch_info = info
        statistic_data = Statistics.objects(product_type=product_type, batch_info=batch_info).first()
        if statistic_data is not None:
            json_data = statistic_data.to_json()
        else:
            json_data = json.dumps(statistic_data)
        print(json_data)
        return json_data
    
    
    
