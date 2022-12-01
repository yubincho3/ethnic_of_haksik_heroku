from datetime import datetime
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

## 시간을 KST로 맞춰야 함
def getTodayWeekday():
    raise NotImplementedError()
    datetime.now()
    return weekdays[datetime.today().weekday()]
