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
    start_at = DateTimeField()
    first_point_at = DateTimeField()
    last_point_at = DateTimeField()
    end_at = DateTimeField()
    unproductive_time_init = StringField(default='00:00')
    unproductive_time_end = StringField(default='00:00')
    productive_time = StringField(default='00:00')
    work_time = StringField(default='00:00')
    on_hold_time = StringField(default='00:00')
    overtime = StringField(default='00:00')
    intra_day = StringField(default='00:00')

class WorkingDay(EmbeddedDocument):
    summary = EmbeddedDocumentField(Summary)
    details = ListField(EmbeddedDocumentField(WorkingDayDetail))

class DriverWorkingDay(Document):
    driver = ObjectIdField(required=True)
    working_day = EmbeddedDocumentField(WorkingDay)
    orders = ListField(ObjectIdField())