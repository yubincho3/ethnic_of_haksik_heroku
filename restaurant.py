import enum

from weekday import *

class Restaurants(enum.Enum):
    Hanwool          = '한울식당(법학관 지하1층)'
    Hakseng          = '학생식당'
    Gyojikwon        = '교직원식당'
    Cheonghyang_Han  = '청향(한식당)'
    Cheonghyang_Yang = '청향(양식당)'
    K_Bobplus        = 'K-Bob+'

CORNER_NAMES = {
    Restaurants.Hanwool: ['2코너 NOODLE', '3코너 CUTLET', '4코너 RICE.oven', '5코너 GUKBOB.Chef'],
    Restaurants.Hakseng: [
        '가마중식', '누들송(면) 중식', '누들송(카페테리아) 중식',
        '인터쉐프 중식', '데일리밥 중식', '가마 석식', 
        '인터쉐프 석식', '데일리밥 석식', '차이웨이'
    ],
    Restaurants.Gyojikwon: ['키친1', '키친2', '오늘의샐러드', '석식'],
    Restaurants.Cheonghyang_Han: ['메뉴1', '메뉴2', '메뉴3', '메뉴4'],
    Restaurants.Cheonghyang_Yang: ['PASTA', 'RISOTTO', 'STEAK'],
    Restaurants.K_Bobplus: ['간편도시락', '김밥']
}

class Time:
    # 시작시간, 종료시간을 tuple로 받습니다.
    # 튜플의 형식은 (시, 분) 입니다.
    def __init__(self, start: tuple, end: tuple):
        self.start = start
        self.end = end

    # 불가능한 시간과 영업시간을 비교하여
    # 현재 메뉴를 먹을 수 있는지에 대한 여부를 bool로 반환합니다.
    def isAble(self, unableTimes: list[tuple]) -> bool:
        hour, minute = self.start

        while (hour, minute) != self.end:
            if (hour, minute) not in unableTimes:
                return True

            minute += 30
            if minute == 60:
                hour += 1
                minute = 0

        return False

HANWOOL_LUNCH = Time((11, 0), (14, 0))
HANWOOL_DINNER = Time((16, 0), (18, 30))
HANWOOL_BOTH = Time(HANWOOL_LUNCH.start, HANWOOL_DINNER.end)

HAKSENG_BREAKFAST = Time((8, 0), (10, 0))
HAKSENG_LUNCH = Time(HAKSENG_BREAKFAST.end, (15, 0))
HAKSENG_DINNER = Time((17, 0), (18, 30))
HAKSENG_CHAIWAY = Time((11, 30), (14, 0))

GYOJIKWON_LUNCH = Time((11, 30), (14, 0))
GYOJIKWON_DINNER = Time((17, 0), (18, 30))

CHEONGHYANG_LUNCH = Time((11, 30), (14, 0))
CHEONGHYANG_DINNER = Time((17, 0), (18, 30))

class Menu:
    def __init__(self, time: Time, menu: str, cost: int):
        self.time = time
        self.menu = menu
        self.cost = cost

    def isAble(self, unableTimes: list[tuple]) -> bool:
        return self.time.isAble(unableTimes)

    def __str__(self) -> str:
        return f'{self.menu}({self.cost}원)'

class Corner:
    def __init__(self, name: str):
        self.name = name
        self.menu = {weekday: list[Menu]() for weekday in Weekday}

    # 해당 요일에 메뉴를 추가합니다.
    # weekday: 요일
    # time: 중식 or 석식
    # menu: 메뉴 이름
    # cost: 가격
    def addMenu(self, weekday: Weekday, time: Time, menu: str, cost: int):
        self.menu[weekday].append(Menu(time, menu, cost))

    # 불가능한 시간과 영업시간을 비교하여 먹을 수 있는 메뉴를 반환합니다.
    def getAbleMenu(self, unableTimes: list[tuple]) -> list[Menu]:
        today = getTodayWeekday()
        todayMenu = self.menu[today]

        ret = [m for m in todayMenu if m.isAble(unableTimes)]

        return ret

class Restaurant:
    def __init__(self, nameEnum: Restaurants):
        self.corners = {corner: Corner(corner) for corner in CORNER_NAMES[nameEnum]}
        self.name = nameEnum.name

    # 현재 레스토랑의 코너들을 리스트로 가져옵니다.
    def getCornerList(self):
        return self.corners.values()

    # 해당 코너에 메뉴를 추가합니다.
    # corner: 코너 이름
    # weekday: 요일
    # time: 중식 or 석식
    # menu: 메뉴 이름
    # cost: 가격
    def addMenu(self, corner: str, weekday: Weekday, time: Time, menu: str, cost: int):
        self.corners[corner].addMenu(weekday, time, menu, cost)
