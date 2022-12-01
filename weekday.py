from datetime import datetime
from pytz import timezone
import enum

class Weekday(enum.Enum):
    Mon = 0
    Tue = 1
    Wed = 2
    Thu = 3
    Fri = 4
    Sat = 5
    Sun = 6
weekdays = [*Weekday]

def getTodayWeekday():
    weekday = datetime.now(timezone('Asia/seoul')).weekday()
    return weekdays[weekday]
