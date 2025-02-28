import datetime
from .daystore import DayStore

class Calendar:
    def __init__(self, store: DayStore):
        self.store = store
    def get_month_days(self, year=None, month=None):
        """
        Return a list of Day objects in the given year/month.
        If year/month are omitted, default to current year/month.
        """
        if year is None:
            year = datetime.date.today().year
        if month is None:
            month = datetime.date.today().month
        start_date = datetime.date(year, month, 1)

        if month == 12:
            next_month_start = datetime.date(year + 1, 1, 1)
        else:
            next_month_start = datetime.date(year, month + 1, 1)

            # The day before next_month_start is the last day of the current month
        end_date = next_month_start - datetime.timedelta(days=1)

        # Make sure the store has days for that range
        self.store.generate_range(start_date.isoformat(), end_date.isoformat())

        # Collect them in a list, sorted by date
        result = []
        current = start_date
        while current <= end_date:
            day_obj = self.store.get_day(current.isoformat())
            if day_obj:
                result.append(day_obj)
            current += datetime.timedelta(days=1)

        return result

    def get_week_days(self, year=None, month=None, week_number=None):
        """
        Return a list of Day objects for a given "week number" in a specific year/month.
        This is flexible: define how 'week_number' is determined for your use case.
        """
        # For demonstration, let's say we do a 7-day chunk of the month:
        if year is None:
            year = datetime.date.today().year
        if month is None:
            month = datetime.date.today().month
        if week_number is None:
            # default: the week containing today's date
            today = datetime.date.today()
            if today.year == year and today.month == month:
                # let's pick a simple approach: 1-based indexing for day-of-month,
                # then figure out which 'week' that is in the month
                day_in_month = today.day
            else:
                day_in_month = 1
            week_number = ((day_in_month - 1) // 7) + 1

        # If you have a more robust approach for "week in a month", e.g. ISO weeks, you'd handle that differently.

        start_day = ((week_number - 1) * 7) + 1  # e.g. week 1 => day=1, week 2 => day=8, etc.
        start_date = datetime.date(year, month, start_day)

        # We want 7 days from that starting point, but don't go beyond the month’s end
        # We'll reuse some logic from get_month_days if needed

        # figure out how many days in that month
        next_month = month + 1
        next_year = year
        if next_month == 13:
            next_month = 1
            next_year = year + 1
        next_month_start = datetime.date(next_year, next_month, 1)
        end_of_month = next_month_start - datetime.timedelta(days=1)

        end_date = start_date + datetime.timedelta(days=6)
        if end_date > end_of_month:
            end_date = end_of_month

        # Make sure the store has this range
        self.store.generate_range(start_date.isoformat(), end_date.isoformat())

        result = []
        current = start_date
        while current <= end_date:
            day_obj = self.store.get_day(current.isoformat())
            if day_obj:
                result.append(day_obj)
            current += datetime.timedelta(days=1)
        return result

    def get_custom_range(self, start_date_str, end_date_str):
        """
        Return a list of Day objects for any custom date range.
        """
        self.store.generate_range(start_date_str, end_date_str)

        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

        result = []
        current = start_date
        while current <= end_date:
            day_obj = self.store.get_day(current.isoformat())
            if day_obj:
                result.append(day_obj)
            current += datetime.timedelta(days=1)

        return result

    def __repr__(self):
        return "<Calendar facade around DayStore>"
