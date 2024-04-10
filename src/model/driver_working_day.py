import datetime
from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import DateTimeField, EmbeddedDocumentField, StringField, ListField, ObjectIdField

class Summary(EmbeddedDocument):
    work_time               = StringField(default='00:00')
    unproductive_time       = StringField(default='00:00')
    productive_time         = StringField(default='00:00')
    on_hold_time            = StringField(default='00:00')
    intra_day               = StringField(default='00:00')
    inter_day               = StringField(default='00:00')
    overtime                = StringField(default='00:00')
    
class Route(EmbeddedDocument):
    id                      = ObjectIdField(required=True)
    description             = StringField()
    color                   = StringField()
    subenterprise           = ObjectIdField()
    
class WorkingDayDetail(EmbeddedDocument):
    id                      = ObjectIdField(required=True)
    start_at                = DateTimeField(null=True)
    first_point_at          = DateTimeField(null=True)
    last_point_at           = DateTimeField(null=True) 
    end_at                  = DateTimeField(null=True)
    direction               = StringField()
    route                   = EmbeddedDocumentField(Route)
    unproductive_time_init  = StringField(default='00:00')
    unproductive_time_end   = StringField(default='00:00')
    productive_time         = StringField(default='00:00')
    work_time               = StringField(default='00:00')
    on_hold_time            = StringField(default='00:00')
    overtime                = StringField(default='00:00')
    intra_day               = StringField(default='00:00')

class Accomplished(EmbeddedDocument):
    summary                 = EmbeddedDocumentField(Summary)
    details                 = ListField(EmbeddedDocumentField(WorkingDayDetail))

class Foreseen(EmbeddedDocument):
    summary                 = EmbeddedDocumentField(Summary)
    details                 = ListField(EmbeddedDocumentField(WorkingDayDetail))

class DriverWorkingDay(Document):
    
    meta = {'collection': 'driver_working_days'}
    
    driver                  = ObjectIdField(required=True)
    enterprise              = ObjectIdField()
    scheduled_at            = DateTimeField()
    accomplished            = EmbeddedDocumentField(Accomplished)
    foreseen                = EmbeddedDocumentField(Foreseen)
    created_at              = DateTimeField(default=datetime.datetime.now)
    updated_at 		        = DateTimeField(null=True)