import datetime
import json

class Day:
    """
    A simple class to represent one day in the calendar as 'YYYY-MM-DD'.
    Each Day has a list of goals (which could be simple strings or custom objects)
    """
    def __init__(self,dt_str):
        try:
            self._date = datetime.datetime.strptime(dt_str,"%Y-%m-%d").date()
        except ValueError:
            raise ValueError("invalid dt_str")
        self.dt_str = dt_str
        self.goals = []
        self.year = self._date.year
        self.month_num = self._date.month                  # 1..12
        self.month_name = self._date.strftime("%B")        # e.g., "March"
        self.day_num = self._date.day
        self.day_of_week_index = self._date.weekday()  # Monday=0, Sunday=6
        self.day_of_week_name = self._date.strftime("%A")

    def add_goal(self, goal):
        """
        Add a goal (could be a string or more advanced class).
        """
        self.goals.append(goal)

    def __repr__(self):
        return (
            f"<Day {self.dt_str} "
            f"({self.day_of_week_name}), "
            f"Month={self.month_name}({self.month_num}), "
            f"DayNum={self.day_num}, "
            f"Goals={len(self.goals)}>"
        )

