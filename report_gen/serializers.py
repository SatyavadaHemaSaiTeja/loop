from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    store_id = serializers.IntegerField()
    uptime_last_hour = serializers.FloatField()
    uptime_last_day = serializers.FloatField()
    uptime_last_week = serializers.FloatField()
    downtime_last_hour = serializers.FloatField()
    downtime_last_day = serializers.FloatField()
    downtime_last_week = serializers.FloatField()
