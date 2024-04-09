from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField, StringField, DictField, DateTimeField, ObjectIdField

class WorkingDay(Document):
    driver = ObjectIdField(required=True)
    orders = ListField(ObjectIdField())