from mongoengine import Document, EmbeddedDocument, fields
from datetime import datetime

class Location(EmbeddedDocument):
    latitude = fields.FloatField(required = True)
    longitude = fields.FloatField(required = True)
    country = fields.StringField(required = True)

class CyberAttack(Document):
    source_location = fields.EmbeddedDocumentField(Location)
    destination_location = fields.EmbeddedDocumentField(Location)
    attack_type = fields.StringField(required = True)
    severity = fields.IntField(required = True)
    timestamp = fields.DateTimeField(required = True)
    additional_details = fields.DictField()

class NotificationRule(Document):
    name = fields.StringField(required = True)
    attack_type = fields.StringField()
    country = fields.StringField()
    min_severity = fields.IntField()
    max_severity = fields.IntField()
    active = fields.BooleanField(default = True)
    created_at = fields.DateTimeField(default = datetime.now)
    threshold_count = fields.IntField(required=False)         
    time_window_minutes = fields.IntField(required=False)       
    cooldown_minutes = fields.IntField(default=10)              
    last_triggered_at = fields.DateTimeField(default=None)      

class Notification(Document):
    rule_name = fields.StringField(required = True)
    attack_id = fields.StringField(required = True)
    triggered_at = fields.DateTimeField(default = datetime.now)
    details = fields.DictField()

