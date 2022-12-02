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

# 오늘의 요일을 가져옵니다.(KST 기준)
def getTodayWeekday():
    weekday = datetime.now(timezone('Asia/seoul')).weekday()
    return weekdays[weekday]
