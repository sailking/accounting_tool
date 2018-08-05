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
    product_id = IntField(unique=True)
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
            for product in data:
                pprint(product)
                item = Purchase.objects(product_id=product["product_id"]).first()
                if item is None:
                    print("create new")
                    item = Purchase()

                item.product_id = product["product_id"]
                item.product_name = product["product_name"]
                item.product_count = int(product["product_count"])
                item.single_original_price = float(product["single_original_price"])
                item.discount = float(product["discount"])
                item.single_buy_price = float(product["single_buy_price"])
                item.total_buy_price = float(product["total_buy_price"])
                item.single_sell_price = float(product["single_sell_price"])
                item.total_sell_price = float(product["total_sell_price"])
                item.single_profit = float(product["single_profit"])
                item.total_profit = float(product["total_profit"])
                item.date = product["date"]
                item.batch_info = product["batch_info"]
                item.postage = 0.0
                   
                item.save()
                
            return "数据保存成功"
        except Exception as e:
            print(e)
    
    @classmethod
    def get_batch(cls, batch_name):
        print("call get_batch")
        products = Purchase.objects(batch_info=batch_name)
        json_data = products.to_json()
        return json_data
    
class Products(DynamicDocument):
    product_id = IntField()
    product_name = StringField(unique=True)
    single_original_price = FloatField()
    discount = FloatField()
    product_count = IntField()
    total_buy_price = FloatField()
    product_type = StringField()
    
    @classmethod
    def get_product_type_list(cls):
        product_types = Products.objects.distinct(field="product_type")
        product_types_list = []
        if product_types is not None:
            for type in product_types:
                print(type.product_type)
                product_types_list.append(type.product_type)
        return json.dumps(product_types_list)
        
    
    
    
    