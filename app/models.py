import os
import sys
from datetime import datetime

import pymongo 
import mongoengine
from mongoengine.document import DynamicDocument
from mongoengine.fields import StringField, IntField, FloatField, DateTimeField

class Purchase(DynamicDocument):
    product_name = StringField()
    date = DateTimeField()
    count = IntField()
    normal_price = FloatField()
    discount = FloatField()
    actual_price = FloatField()
    sell_price = FloatField()
    postage = FloatField()
    box = StringField()
    