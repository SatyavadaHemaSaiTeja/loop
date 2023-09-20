from datetime import datetime, timedelta, time
from pytz import timezone
from .models import StoreTimezone, StoreBusinessHours, StoreStatus


def compute_uptime_for_interval(store_id, start_time, end_time):
    store_tz = timezone(StoreTimezone.objects.get_timezone(store_id))
    local_start_time = start_time.astimezone(store_tz)
    local_end_time = end_time.astimezone(store_tz)

    business_hours = StoreBusinessHours.objects.get_hours_for_day(store_id, local_start_time.weekday())

    if not business_hours:
        business_start_time = time(0, 0)
        business_end_time = time(23, 59, 59)
    else:
        business_start_time = business_hours.start_time_local
        business_end_time = business_hours.end_time_local

    local_start_time = max(local_start_time, datetime.combine(local_start_time.date(), business_start_time))
    local_end_time = min(local_end_time, datetime.combine(local_end_time.date(), business_end_time))

    status_logs = list(
        StoreStatus.objects.get_status_between(store_id, local_start_time, local_end_time).order_by('timestamp_utc'))

    uptime_minutes = 0
    downtime_minutes = 0

    if status_logs:
        prev_log = status_logs[0]
        for current_log in status_logs[1:]:
            interval_minutes = (current_log.timestamp_utc - prev_log.timestamp_utc).seconds / 60
            if prev_log.status == 'active':
                uptime_minutes += interval_minutes
            else:
                downtime_minutes += interval_minutes
            prev_log = current_log

        # Interpolate for the periods before the first log and after the last log within business hours
        if prev_log.status == 'active':
            uptime_minutes += (local_end_time - prev_log.timestamp_utc).seconds / 60
            uptime_minutes += (status_logs[0].timestamp_utc - local_start_time).seconds / 60
        else:
            downtime_minutes += (local_end_time - prev_log.timestamp_utc).seconds / 60
            downtime_minutes += (status_logs[0].timestamp_utc - local_start_time).seconds / 60

    return uptime_minutes, downtime_minutes


def generate_report():
    now = datetime.utcnow()
    last_hour = now - timedelta(hours=1)
    last_day = now - timedelta(days=1)
    last_week = now - timedelta(weeks=1)

    report_data = []

    for store in StoreTimezone.objects.all():
        store_id = store.store_id
        uptime_hour, downtime_hour = compute_uptime_for_interval(store_id, last_hour, now)
        uptime_day, downtime_day = compute_uptime_for_interval(store_id, last_day, now)
        uptime_week, downtime_week = compute_uptime_for_interval(store_id, last_week, now)

        report_data.append({
            "store_id": store_id,
            "uptime_last_hour": uptime_hour,
            "uptime_last_day": uptime_day / 60,
            "uptime_last_week": uptime_week / 60,
            "downtime_last_hour": downtime_hour,
            "downtime_last_day": downtime_day / 60,
            "downtime_last_week": downtime_week / 60
        })

    return report_data
