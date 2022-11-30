from bs4 import BeautifulSoup
import requests

from restaurant import *

# 이번 주의 메뉴를 크롤링합니다.
# Restaraunt 객체의 리스트를 반환합니다.
def crawlThisWeeksMenu(url: str) -> list[Restaurant]:
    # 식당별 객체가 저장될 리스트
    restaurantList = []

    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.HTTPError as e:
        print(e)
        return []

    bs = BeautifulSoup(res.text, 'lxml')

    # 메뉴판 'name' property가 전부 'aa'? 하드코딩으로...
    menuTexts = [e.get('value') for e in bs.find_all('input', {'name': 'aa'})]

    # -------------한울식당--------------
    cornerIdx = 0  # 현재 식당의 코너 인덱스(CORNER_NAMES)
    weekdayCnt = Weekday.Mon.value # 식당 메뉴판 요일

    cornerName = CORNER_NAMES[Restaraunts.Hanwool][cornerIdx]
    hanwool = Restaurant(Restaraunts.Hanwool)
    idx = 30 # 메뉴 텍스트들의 리스트의 인덱스

    for _ in range(19):
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

        hanwool.addMenu(cornerName, weekdays[weekdayCnt], businessHour, menu, int(cost))

        if weekdayCnt == Weekday.Fri.value:
            weekdayCnt = Weekday.Mon.value
            cornerIdx += 1
            cornerName = CORNER_NAMES[Restaraunts.Hanwool][cornerIdx]
        else:
            weekdayCnt += 1

    # 한울식당의 Gukbab.chef에 대해서는 따로 처리
    cornerName = CORNER_NAMES[Restaraunts.Hanwool][cornerIdx]
    weekdayCnt = Weekday.Mon.value
    idx += 4

    for _ in range(5):
        dinnerStrIdx = menuTexts[idx].find('[석식]')
        lunchStr = menuTexts[idx][:dinnerStrIdx]\
            .replace('{fourName=메뉴, fourValue=', '')\
            .replace('<br>', '')
        dinnerStr = menuTexts[idx][dinnerStrIdx:]\
            .replace('<br>', '')\
            .replace('}', '')

        lunchMenu = lunchStr[:lunchStr.find('￦')]
        lunchCost = lunchStr[lunchStr.find('￦') + 1:]

        if not lunchCost.strip():
            lunchCost = '-1'

        hanwool.addMenu(cornerName, weekdays[weekdayCnt],
            HANWOOL_LUNCH, lunchMenu, int(lunchCost))

        dinnerMenu = dinnerStr[:dinnerStr.find('￦')]
        dinnerCost = dinnerStr[dinnerStr.find('￦') + 1:]

        if not dinnerCost.strip():
            dinnerCost = '-1'

        hanwool.addMenu(cornerName, weekdays[weekdayCnt],
            HANWOOL_DINNER, dinnerMenu, int(dinnerCost))

        weekdayCnt += 1
        idx += 2

    restaurantList.append(hanwool)

    return restaurantList

    # -------------학생식당-------------- NOW TO DO
    cornerIdx = 0
    weekdayCnt = 0

    cornerName = CORNER_NAMES[Restaraunts.Hakseng][0]
    hakseng = Restaurant(Restaraunts.Hakseng)
    idx += 18

    for _ in range(77):
        menu = menuTexts[idx]\
            .replace('{fourName=메뉴, fourValue=', '')[:-1]\
            .replace('<br>', ', ')\
            .strip(', ')
        cost = menuTexts[idx + 1]\
            .replace('{fourName=가격, fourValue=', '')\
            .replace('<span class=\'orange_txt\'>￦', '')\
            .replace('</span>', '')\
            .replace('<br>', '')\
            .strip()[:-1]
        idx += 2
        print(menu)
        input(cost)
        if menu:
            continue

        #if cornerIdx == CORNER_NAMES[Restaraunts.Hakseng].index('')

        input(cost)


    # 교직원식당
    # for i in range(28):

    # 청향(한식당)
    # for i in range(49):

    # 청향(양식당)
    # for i in range(28):

    # 생활관식당은 넘어간다.
    # idx += 42

    # K-Bob+
    # for i in range(5):

#for i in crawlThisWeeksMenu('https://www.kookmin.ac.kr/user/unLvlh/lvlhSpor/todayMenu/index.do'):
#    print(i)
