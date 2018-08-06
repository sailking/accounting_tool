# *-* coding=utf-8 *-*

import os
import sys
from datetime import datetime
from pprint import pprint
import configparser
import json

import pymongo 
import mongoengine
from mongoengine.document import DynamicDocument
from mongoengine.fields import StringField, IntField, FloatField, DateTimeField
from numpy.lib import stride_tricks
from ipywidgets.widgets.widget_float import FloatSlider


def connect_database():
        cf = configparser.ConfigParser()
        cf.read("config.cfg")
        db = mongoengine.connect(db = cf.get("Database", "db"),
                                 host = cf.get("Database", "host"))
        
class Purchase(DynamicDocument):
    product_id = IntField()
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
    postage = FloatField()
    packaging = FloatField()
    batch_info = StringField()
    
    @classmethod
    def seed(cls, data):
        print("call save")
        try:
            for purchase in data:
                pprint(purchase)
                item = Purchase.objects(product_id=purchase["product_id"], batch_info=purchase["batch_info"]).first()
                if item is None:
                    print("create new")
                    item = Purchase()

                item.product_id = purchase["product_id"]
                item.product_name = purchase["product_name"]
                item.product_count = int(purchase["product_count"])
                item.single_original_price = float(purchase["single_original_price"])
                item.discount = float(purchase["discount"])
                item.single_buy_price = float(purchase["single_buy_price"])
                item.total_buy_price = float(purchase["total_buy_price"])
                item.single_sell_price = float(purchase["single_sell_price"])
                item.total_sell_price = float(purchase["total_sell_price"])
                item.single_profit = float(purchase["single_profit"])
                item.total_profit = float(purchase["total_profit"])
                item.date = purchase["date"]
                item.batch_info = purchase["batch_info"]
                item.postage = 0.0
                   
                item.save()
                
            return "数据保存成功"
        except Exception as e:
            print(e)
    
    @classmethod
    def get_batch_list(cls):
        batch_list = Purchase.objects.distinct(field="batch_info")
        print(batch_list)
        return json.dumps(batch_list)
        
    @classmethod
    def get_purchase(cls, batch_name):
        products = Purchase.objects(batch_info=batch_name)
        json_data = products.to_json()
        return json_data
    
    @classmethod
    def purchase_delete(cls):
        pass
    
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
                pprint(product)
                item = Products.objects(product_name=product["product_name"]).first()
                if item is None:
                    print("create new product")
                    item = Products()
                item.product_id = product["product_id"]
                item.product_name = product["product_name"]
                item.single_original_price = float(product["single_original_price"])
                item.discount = float(product["discount"])
                item.product_type = product["product_type"]
                
                item.save()
            return "数据保存成功"
        except Exception as e:
            print(e)
            return e
        
        
    
    
    
    
