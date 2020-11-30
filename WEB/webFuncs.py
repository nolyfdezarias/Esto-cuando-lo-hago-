
import datetime

def makeWeek(initDay):
    week = []
    _date = initDay.split("-")

    _day = int(_date[0])
    _month = int(_date[1])
    _year = int(_date[2])

    for i in range(7):

        week.append([])

        for j in range(8,16):
            week[i].append( (datetime.datetime(_year,_month,_day,j) , datetime.datetime(_year,_month,_day,j + 1) , vanilla_activity ) )
    

    return week
