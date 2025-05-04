from mongoengine import Document, EmbeddedDocument, fields

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

