import datetime

from custom_exceptions import DateFormatException

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

def parse_date_from_string(datestring):
    """Parses dates in various formats to datetime.date object"""

    try:
        return datetime.datetime.fromisoformat(datestring).date()

    except ValueError:

        if "-" in datestring:
            year, month, day = datestring.split("-")
            sep = "-"
        elif "." in datestring:
            day, month, year = datestring.split(".")
            sep = "."
        else:
            raise DateFormatException

        if len(year) == 2:
            year_format = "%y"
        elif len(year) == 4:
            year_format = "%Y"

        if sep == "-":
            parsing_format = f"{year_format}{sep}%m{sep}%d"
        elif sep == ".":
            parsing_format = f"%d{sep}%m{sep}{year_format}"

        return datetime.datetime.strptime(datestring, parsing_format).date()



