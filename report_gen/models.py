from django.db import models


class StoreTimezoneManager(models.Manager):
    def get_timezone(self, store_id):
        return self.filter(store_id=store_id).first().timezone_str or "America/Chicago"


class StoreBusinessHoursManager(models.Manager):
    def get_hours_for_day(self, store_id, day_of_week):
        return self.filter(store_id=store_id, dayOfWeek=day_of_week).first()


class StoreStatusManager(models.Manager):
    def get_status_between(self, store_id, start_time, end_time):
        return self.filter(store_id=store_id, timestamp_utc__range=(start_time, end_time))


class StoreTimezone(models.Model):
    store_id = models.IntegerField()
    timezone_str = models.CharField(max_length=50, default="America/Chicago")

    objects = StoreTimezoneManager()


class StoreBusinessHours(models.Model):
    store_id = models.IntegerField()
    dayOfWeek = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    objects = StoreBusinessHoursManager()


class StoreStatus(models.Model):
    store_id = models.IntegerField()
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10)

    objects = StoreStatusManager()
