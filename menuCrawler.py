from bs4 import BeautifulSoup
import requests
import re

from restaurant import *

CRAWL_URL = 'https://www.kookmin.ac.kr/user/unLvlh/lvlhSpor/todayMenu/index.do'

# 이번 주의 메뉴를 크롤링합니다.
# Restaraunt 객체의 리스트를 반환합니다.
def crawlThisWeeksMenu(url: str = CRAWL_URL) -> list[Restaurant]:
    # 식당별 객체가 저장될 리스트
    restaurantList = []

    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.HTTPError as e:
        print(e)
        return []

    bs = BeautifulSoup(res.text, 'html.parser')

    # 메뉴판 'name' property가 전부 'aa'? 하드코딩으로...
    menuTexts = [e.get('value') for e in bs.find_all('input', {'name': 'aa'})]

    # -------------한울식당-------------- #
    hanwool = Restaurant(Restaurants.Hanwool)

    cornerIdx = 0    # 현재 식당의 코너 인덱스(CORNER_NAMES)
    cornerName = CORNER_NAMES[Restaurants.Hanwool][cornerIdx]

    weekdayCnt = Weekday.Mon.value  # 식당 메뉴판 요일
    idx = 30    # 메뉴 텍스트들의 리스트의 인덱스

    # 2코너(NOODLE) ~ 4코너(RICE.oven)
    for _ in range(19):
        try:
            menu = menuTexts[idx]\
                .replace('{fourName=메뉴, fourValue=', '')\
                .replace('주말운영없음', '')\
                .replace('<br>', '')\
                .strip()[:-1]
            cost = menuTexts[idx + 1]\
                .replace('{fourName=가격, fourValue=', '')\
                .replace('<span class=\'orange_txt\'>￦', '')\
                .replace('</span>', '')\
                .replace('<br>', '')\
                .strip()[:-1]
            idx += 2

            if menu.find('중식') != -1: # 중식 only
                businessHour = HANWOOL_LUNCH
            elif menu.find('중석식') != -1: # 중식 & 석식
                businessHour = HANWOOL_BOTH
            else:
                continue

            if not cost.strip():
                cost = '-1'
        except: pass
        else:
            hanwool.addMenu(cornerName, weekdays[weekdayCnt], businessHour, menu, int(cost))

        weekdayCnt += 1

        if weekdayCnt == Weekday.Sat.value:
            weekdayCnt = 0
            cornerIdx += 1
            if cornerIdx < len(CORNER_NAMES[Restaurants.Hanwool]):
                cornerName = CORNER_NAMES[Restaurants.Hanwool][cornerIdx]

    # Gukbab.chef
    cornerName = CORNER_NAMES[Restaurants.Hanwool][cornerIdx]

    weekdayCnt = Weekday.Mon.value
    idx += 4

    for _ in range(5):
        try:
            dinnerStrIdx = menuTexts[idx].find('[석식]')
            lunchStr = menuTexts[idx][:dinnerStrIdx]\
                .replace('{fourName=메뉴, fourValue=', '')\
                .replace('<br>', '')
            dinnerStr = menuTexts[idx][dinnerStrIdx:]\
                .replace('<br>', '')\
                .replace('}', '')

            i = 0
            while i < len(lunchStr):
                menu = ''
                cost = ''

                while i < len(lunchStr) and lunchStr[i] != '￦':
                    menu += lunchStr[i]
                    i += 1

                i += 1
                while i < len(lunchStr) and lunchStr[i].isdigit():
                    cost += lunchStr[i]
                    i += 1

                if not cost.strip():
                    cost = '-1'

                if menu.strip():
                    if menu[0] != '[':
                        menu = '[중식]' + menu
                    hanwool.addMenu(cornerName, weekdays[weekdayCnt],
                        HANWOOL_LUNCH, menu, int(cost))

            i = 0
            while i < len(dinnerStr):
                menu = ''
                cost = ''

                while i < len(dinnerStr) and dinnerStr[i] != '￦':
                    menu += dinnerStr[i]
                    i += 1

                i += 1
                while i < len(dinnerStr) and dinnerStr[i].isdigit():
                    cost += dinnerStr[i]
                    i += 1

                if not cost.strip():
                    cost = '-1'

                if menu.strip():
                    if menu[0] != '[':
                        menu = '[석식]' + menu
                    hanwool.addMenu(cornerName, weekdays[weekdayCnt],
                        HANWOOL_DINNER, menu, int(cost))
        except: pass

        weekdayCnt += 1
        idx += 2

    restaurantList.append(hanwool)

    # -------------학생식당-------------- #
    hakseng = Restaurant(Restaurants.Hakseng)

    cornerIdx = 0
    cornerName = CORNER_NAMES[Restaurants.Hakseng][cornerIdx]

    weekdayCnt = Weekday.Sun.value
    idx += 30

    # 가마 중식 ~ 데일리밥 중식
    for _ in range(35):
        try:
            menu = menuTexts[idx].replace('{fourName=메뉴, fourValue=', '')[:-1]
            cost = menuTexts[idx + 1]\
                .replace('{fourName=가격, fourValue=', '')\
                .replace('<span class=\'orange_txt\'>￦', '')\
                .replace('</span>', '')\
                .replace('<br>', '')\
                .strip()[:-1]
            idx += 2

            menu = re.sub('(<br>)+', ', ', menu).strip(', ')

            if not menu.strip() or menu[0] == '※':
                raise Exception()

            if not cost.strip():
                cost = '-1'
        except: pass
        else:
            hakseng.addMenu(cornerName, weekdays[weekdayCnt], 
                HAKSENG_LUNCH, menu, int(cost))

        weekdayCnt = (weekdayCnt + 1) % 7

        if weekdayCnt == Weekday.Sun.value:
            cornerIdx += 1
            if cornerIdx < len(CORNER_NAMES[Restaurants.Hakseng]):
                cornerName = CORNER_NAMES[Restaurants.Hakseng][cornerIdx]

    # 가마 석식 ~ 데일리밥 석식
    for _ in range(21):
        try:
            menu = menuTexts[idx].replace('{fourName=메뉴, fourValue=', '')[:-1]
            cost = menuTexts[idx + 1]\
                .replace('{fourName=가격, fourValue=', '')\
                .replace('<span class=\'orange_txt\'>￦', '')\
                .replace('</span>', '')\
                .replace('<br>', '')\
                .strip()[:-1]
            idx += 2

            menu = re.sub('(<br>)+', ', ', menu).strip(', ')

            if not menu.strip() or menu[0] == '※':
                raise Exception()

            if not cost.strip():
                cost = '-1'
        except: pass
        else:
            hakseng.addMenu(cornerName, weekdays[weekdayCnt], 
                HAKSENG_DINNER, menu, int(cost))

        weekdayCnt = (weekdayCnt + 1) % 7

        if weekdayCnt == Weekday.Sun.value:
            cornerIdx += 1
            if cornerIdx < len(CORNER_NAMES[Restaurants.Hakseng]):
                cornerName = CORNER_NAMES[Restaurants.Hakseng][cornerIdx]

    # 차이웨이
    idx += 2
    menuText = menuTexts[idx].replace('{fourName=메뉴, fourValue=', '')[:-1]
    menuText = re.sub('<br>', '\t', menuText)
    menuText = re.sub('\t+', '\t', menuText)

    menuList = menuText.strip().split()
    for i in range(0, len(menuList), 2):
        for j in Weekday:
            hakseng.addMenu(cornerName, j, HAKSENG_CHAIWAY,
                menuList[i], int(menuList[i + 1]))
    
    restaurantList.append(hakseng)

    # -------------교직원 식당-------------- #
    gyojikwon = Restaurant(Restaurants.Gyojikwon)

    cornerIdx = 0
    cornerName = CORNER_NAMES[Restaurants.Gyojikwon][cornerIdx]

    weekdayCnt = Weekday.Mon.value
    idx += 28

    # 키친1 ~ 오늘의 샐러드
    for _ in range(21):
        try:
            menu = menuTexts[idx].replace('{fourName=메뉴, fourValue=', '')[:-1]
            cost = menuTexts[idx + 1]\
                .replace('{fourName=가격, fourValue=', '')\
                .replace('<span class=\'orange_txt\'>￦', '')\
                .replace('</span>', '')\
                .replace('<br>', '')\
                .strip()[:-1]
            idx += 2

            menu = re.sub('(<br>)+', ', ', menu).strip(', ')

            if not menu.strip() or menu[0] == '※':
                raise Exception()

            if not cost.strip():
                cost = '-1'
        except: pass
        else:
            gyojikwon.addMenu(cornerName, weekdays[weekdayCnt], 
                GYOJIKWON_LUNCH, menu, int(cost))

        weekdayCnt = (weekdayCnt + 1) % 7

        if weekdayCnt == Weekday.Sun.value:
            cornerIdx += 1
            if cornerIdx < len(CORNER_NAMES[Restaurants.Gyojikwon]):
                cornerName = CORNER_NAMES[Restaurants.Gyojikwon][cornerIdx]

    # 석식
    for _ in range(5):
        try:
            menu = menuTexts[idx].replace('{fourName=메뉴, fourValue=', '')[:-1]
            cost = menuTexts[idx + 1]\
                .replace('{fourName=가격, fourValue=', '')\
                .replace('<span class=\'orange_txt\'>￦', '')\
                .replace('</span>', '')\
                .replace('<br>', '')\
                .strip()[:-1]
            idx += 2

            menu = re.sub('(<br>)+', ', ', menu).strip(', ')

            if not menu.strip() or menu[0] == '※':
                raise Exception()

            if not cost.strip():
                cost = '-1'
        except: pass
        else:
            gyojikwon.addMenu(cornerName, weekdays[weekdayCnt], 
                GYOJIKWON_DINNER, menu, int(cost))

        weekdayCnt += 1

    restaurantList.append(gyojikwon)

    # -------------청향(한식당)-------------
    cheonghyang_han = Restaurant(Restaurants.Cheonghyang_Han)

    cornerIdx = 0
    cornerName = CORNER_NAMES[Restaurants.Cheonghyang_Han][cornerIdx]

    weekdayCnt = Weekday.Mon.value
    idx += 4

    for _ in range(27):
        try:
            menu = menuTexts[idx].replace('{fourName=메뉴, fourValue=', '')[:-1]
            menu = re.sub('(<br>)+', ' ', menu)
            menu = re.sub(' +', ' ', menu.strip())
            cost = menuTexts[idx + 1]\
                .replace('{fourName=가격, fourValue=', '')\
                .replace('<span class=\'orange_txt\'>￦', '')\
                .replace('</span>', '')\
                .replace('<br>', '')\
                .strip()[:-1]
            idx += 2

            if not menu.strip():
                raise Exception()

            if not cost.strip():
                cost = '-1'
        except: pass
        else:
            cheonghyang_han.addMenu(cornerName, weekdays[weekdayCnt], 
                CHEONGHYANG_LUNCH, menu, int(cost))
            cheonghyang_han.addMenu(cornerName, weekdays[weekdayCnt], 
                CHEONGHYANG_DINNER, menu, int(cost))

        weekdayCnt = (weekdayCnt + 1) % 7

        if weekdayCnt == Weekday.Sun.value:
            cornerIdx += 1
            if cornerIdx < len(CORNER_NAMES[Restaurants.Cheonghyang_Han]):
                cornerName = CORNER_NAMES[Restaurants.Cheonghyang_Han][cornerIdx]

    restaurantList.append(cheonghyang_han)

    # -------------청향(양식당)-------------
    cheonghyang_yang = Restaurant(Restaurants.Cheonghyang_Yang)

    cornerIdx = 0
    cornerName = CORNER_NAMES[Restaurants.Cheonghyang_Yang][cornerIdx]

    idx += 44
    for _ in range(3):
        menuText = menuTexts[idx].replace('{fourName=메뉴, fourValue=', '')[:-1]\
            .replace('원', '')\
            .replace(',', '')
        menuText = re.sub('(<br>|[)])+', ' ', menuText)
        menuText = re.sub(' +', ' ', menuText.replace(' (', '').strip())

        idx += 14

        menuList = menuText.strip().split()
        for i in range(0, len(menuList), 2):
            for j in range(5):
                cheonghyang_yang.addMenu(cornerName, weekdays[j], CHEONGHYANG_LUNCH,
                    menuList[i], int(menuList[i + 1]))

        cornerIdx += 1
        if cornerIdx < len(CORNER_NAMES[Restaurants.Cheonghyang_Yang]):
            cornerName = CORNER_NAMES[Restaurants.Cheonghyang_Yang][cornerIdx]

    restaurantList.append(cheonghyang_yang)

    # 생활관식당은 넘어간다.
    idx += 42

    # K-Bob+의 운영시간을 저장한다.
    # 만약 K-Bob+의 영업시간이 적혀있지 않다면 영업을 하지 않는 것이므로 바로 리턴한다.
    times = []
    flag = False

    for _ in range(5):
        hours = []

        i = 0
        while i < len(menuTexts[idx]):
            hourString = ''
            while menuTexts[idx][i].isdigit():
                hourString += menuTexts[idx][i]
                i += 1

            if hourString:
                hours.append(int(hourString))

            i += 1

        if not times:
            flag = True
            break

        times.append(Time((hours[0], 0), (hours[1], 0)))
        idx += 2

    if flag:
        return restaurantList

    # -------------K-Bob+-------------
    kbobplus = Restaurant(Restaurants.K_Bobplus)

    cornerIdx = 0
    cornerName = CORNER_NAMES[Restaurants.K_Bobplus][cornerIdx]

    idx += 4
    menuText = menuTexts[idx].replace('{fourName=메뉴, fourValue=', '')[:-1]\
        .replace('<br>', ' ')\
        .replace('￦', '')\
        .replace(',', '')
    menuText = re.sub(' +', ' ', menuText)

    # 간편도시락
    menuList = menuText.strip().split()
    for i in range(0, len(menuList), 2):
        for j in range(5):
            kbobplus.addMenu(cornerName, weekdays[j], times[j],
                menuList[i], int(menuList[i + 1]))

    # 김밥
    cornerIdx += 1
    cornerName = CORNER_NAMES[Restaurants.K_Bobplus][cornerIdx]

    idx += 14
    for i in range(5):
        menuText = menuTexts[idx].replace('{fourName=메뉴, fourValue=', '')[:-1]\
            .replace('<br>', ' ')\
            .replace('￦', '')\
            .replace(',', '')
        menuText = re.sub(' +', ' ', menuText)
        idx += 2

        menuList = menuText.strip().split()
        for j in range(0, len(menuList), 2):
            menu = menuList[j]
            cost = int(menuList[j + 1])

            kbobplus.addMenu(cornerName, weekdays[i], times[i], menu, cost)

    restaurantList.append(kbobplus)

    return restaurantList
