from datetime import date, timedelta
from django.utils.timezone import now

def get_month_range(target_date: date = None):
    """
    Возвращает кортеж (start_date, end_date) для текущего месяца
    или указанной даты.
    """
    if target_date is None:
        target_date = now().date()

    start = target_date.replace(day=1)
    next_month = start.replace(day=28) + timedelta(days=4)
    end = next_month - timedelta(days=next_month.day)
    return start, end
