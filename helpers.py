import datetime


def format_to_german_date(date):
    """Converts a date into a German string date format"""

    if isinstance(date, datetime.date):
        month = date.month
        german_months = {1: "Januar", 2: "Februar", 3: "März", 4: "April", 5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
                         9: "September", 10: "Oktober", 11: "November", 12: "Dezember"}

        return f"{date.strftime('%d.')} {german_months[month]} {date.strftime('%Y')}"

    else:
        return f"Cannot format date {date}"


def determine_payment_target_date(date, payment_horizon_in_days):
    """Determines a target date for payment"""

    if isinstance(date, datetime.date) and isinstance(payment_horizon_in_days, int):

        target_date = date + datetime.timedelta(days=payment_horizon_in_days)
        while target_date.weekday() in [5, 6]:
            target_date += datetime.timedelta(days=1)

        return target_date

    else:
        raise Exception
