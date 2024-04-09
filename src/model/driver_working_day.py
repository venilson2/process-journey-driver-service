import datetime
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField, StringField, DictField, DateTimeField, ObjectIdField

class Summary(EmbeddedDocument):
    work_time = StringField(default='00:00')
    unproductive_time = StringField(default='00:00')
    productive_time = StringField(default='00:00')
    on_hold_time = StringField(default='00:00')
    intra_day = StringField(default='00:00')
    inter_day = StringField(default='00:00')
    overtime = StringField(default='00:00')
    
class WorkingDayDetail(EmbeddedDocument):
    id = ObjectIdField(required=True)
    start_at = DateTimeField(null=True)
    first_point_at = DateTimeField(null=True)
    last_point_at = DateTimeField(null=True) 
    end_at = DateTimeField(null=True)
    unproductive_time_init = StringField(default='00:00')
    unproductive_time_end = StringField(default='00:00')
    productive_time = StringField(default='00:00')
    work_time = StringField(default='00:00')
    on_hold_time = StringField(default='00:00')
    overtime = StringField(default='00:00')
    intra_day = StringField(default='00:00')

class Realized(EmbeddedDocument):
    summary = EmbeddedDocumentField(Summary)
    details = ListField(EmbeddedDocumentField(WorkingDayDetail))

class Foreseen(EmbeddedDocument):
    summary = EmbeddedDocumentField(Summary)
    details = ListField(EmbeddedDocumentField(WorkingDayDetail))

class DriverWorkingDay(Document):
    
    meta = {'collection': 'driver_working_days'}
    
    driver = ObjectIdField(required=True)
    realized = EmbeddedDocumentField(Realized)
    foreseen = EmbeddedDocumentField(Foreseen)
    orders = ListField(ObjectIdField())