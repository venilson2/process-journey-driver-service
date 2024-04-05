import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import DateTimeField, IntField, StringField

class CustomBaseDocument(Document):
	meta = {'abstract': True}

	created_at 			= DateTimeField(default=datetime.datetime.now)
	updated_at 			= DateTimeField()

	def set_all_values(self, data):
		for attr in data:
			if hasattr(self, attr):
				setattr(self, attr, data[attr])