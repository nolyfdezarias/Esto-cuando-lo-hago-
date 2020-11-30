from flask import g

from .funcs import loadFile,try_to_insert,getWeek,getFreeTurns,printWeek,getActivities
from .testcase import act_list1 as testList
from .BuildMj import buildMj
import datetime


def singleAddActivity(new_act,my_week, free_Turns, real_free_Turns, activities, actNumb):
   
    _name,_p,_year,_month,_day,_hour,_min = new_act

    # buscar el dia es de la semana q representa una fecha
    insert_day = datetime.datetime(_year,_month,_day).isoweekday() 


    #construir la matriz de costos asociados a una actividad
    mj = buildMj(_p,datetime.datetime(_year,_month,_day,_hour,_min),insert_day,free_Turns)


    actNumb = actNumb + 1
    activities.append((_name,_p,_year,_month,_day,mj, actNumb,-1))

    #anardir la actividad en la semana
    try_to_insert(free_Turns,activities,insert_day - 1, my_week, real_free_Turns)

    # print("=================ESTA ES LA SALIDA ===========================================")
    # print(type(my_week))
    
    # printWeek(my_week)
    return my_week