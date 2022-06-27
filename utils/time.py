from datetime import datetime, timedelta, timezone


def get_beijing_time():
    utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    beijing_time = utc_time.astimezone(timezone(timedelta(hours=8)))
    return beijing_time
