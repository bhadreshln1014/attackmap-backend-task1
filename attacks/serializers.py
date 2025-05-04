from rest_framework import serializers

class LocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    country = serializers.CharField()

class CyberAttackSerializer(serializers.Serializer):
    source_location = LocationSerializer()
    destination_location = LocationSerializer()
    attack_type = serializers.CharField()
    severity = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    additional_details = serializers.DictField()

class NotificationRuleSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    attack_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    country = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    min_severity = serializers.IntegerField(required=False)
    max_severity = serializers.IntegerField(required=False)
    active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)

class NotificationSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    rule_name = serializers.CharField()
    attack_id = serializers.CharField()
    triggered_at = serializers.DateTimeField()
    details = serializers.DictField()