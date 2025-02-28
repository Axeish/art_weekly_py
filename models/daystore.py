from .day import Day
import datetime

class DayStore:
    def __init__(self):
        self.days = {}

    def get_or_create_day(self, dt_str):
        """
        Return the existing Day object if present, else create a new one.
        """
        if dt_str not in self.days:
            self.days[dt_str] = Day(dt_str)
        return self.days[dt_str]

    def get_day(self, dt_str):
        """Return a Day if it exists, or None."""
        return self.days.get(dt_str)

    def has_day(self, dt_str):
        """Check if a day with dt_str is already stored."""
        return dt_str in self.days

    def generate_range(self, start_date_str, end_date_str):
        """
        Create all days from start_date_str to end_date_str, inclusive.
        If a day already exists, reuse it and do NOT overwrite.
        """
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

        if end_date < start_date:
            raise ValueError("end_date cannot be before start_date")

        current = start_date
        while current <= end_date:
            iso_str = current.isoformat()
            self.get_or_create_day(iso_str)  # ensures day is in store
            current += datetime.timedelta(days=1)

    def __repr__(self):
        return f"<DayStore with {len(self.days)} days>"