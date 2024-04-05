import configparser
import math
import operator
import re
import sys
import pytz
import datetime
from mongoengine import Q
from bson import DBRef, ObjectId

from src.model.order import Order

class ConfigPropertiesHelper(object):
	config = None
	
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read('config.properties')
	
	def get_property_value(self, section, property):
		return self.config.get(section, property)