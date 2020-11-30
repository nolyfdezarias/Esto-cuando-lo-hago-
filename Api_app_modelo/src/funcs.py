
import json
from .hungarianAlgoritm import hungarina_Alg
from .initPULP import runPulp
import datetime

def cleanWeek2 (week):

    for i in range(0, len(week)):
        for j in range(0, len(week[i])):
            _,_,_act = week[i][j]
            if _act.name != None:
                week[i][j] = (L[i][j][0], L[i][j][1], vanilla_activity)


def loadFile(myfile,week):
    
    activity_list = []
    activity_list_no_begin = [] # actividades sin comienzo

    with open(f'jsons/{myfile}') as file:
        data = json.load(file)

        i = 0
        for x in data:
            _date = x["date"]
            _begin = x["time"]
            _end = x["end_time"]
            _name = x["name"]
            
            _date = _date.split('-') # Ej (["anno","mes","dia"])
            if _begin == None : #Actividad sin hora de inicio
                activity_list_no_begin.append((_date,_name))
            
            else: #Actividad con Hora de Inicio
                _begin = _begin.split(':')
                end_time = None
                #Si la activiad no tiene hora de finalizacion se le asignara un valor nulo, que sera tratado
                #de una manera especial al insertarla,en otras palabras si la hora de finalizacion es nula
                #la duracion del turno estara determinada por el turno que empiece a la hora de inicio de 
                #dicha actividad
                if _end != None: # Actividad con Hora de finalizacion
                    _end= _end.split(':')
                    end_time = datetime.datetime(int(_date[0]) , int(_date[1]) , int (_date[2]),int(_end[0]), int(_end[1]))
                activity_list.append(Activity( date = datetime.datetime(int(_date[0]) , int(_date[1]) , int (_date[2]))  , 
                                           begin_time = datetime.datetime(int(_date[0]) , int(_date[1]) , int (_date[2]),int(_begin[0]), int(_begin[1])),
                                           end_time = end_time,name = _name)  )
    for x in activity_list: #primero se ubican las actividades que tienen hora inicio
        _day = x.date.isoweekday() - 1
        insert_activity(week[_day],x)
   
    for x in activity_list_no_begin: # insertar actividades que no tienen hora de inicio
        _date,_name = x
        
        _day = datetime.datetime(int(_date[0]),int(_date[1]),int(_date[2])).isoweekday() - 1

        for turn in range(0,len(week[_day])):#Recorrer todos los turnos del dia de la actividad sin inicio
            _begin,_end,_act = week[_day][turn]
            if _act.name == None:#Si el turn(i) no tiene alguna actividad asignada
                week[_day][turn] = (_begin,_end,Activity(_date,_begin,_end,_name))
                break



'''
def loadFile(myfile,week):
    
    activity_list = []
    activity_list_no_begin = [] # actividades sin comienzo

    with open(myfile) as file:
        data = json.load(file)

        i = 0
        for x in data:
            _date = x["date"]
            _begin = x["time"]
            _end = x["end_time"]
            _name = x["name"]
            
            _date = _date.split('-') # Ej (["anno","mes","dia"])
            if _begin == None : #Actividad sin hora de inicio
                activity_list_no_begin.append((_date,_name))
            
            else: #Actividad con Hora de Inicio
                _begin = _begin.split(':')
                end_time = None
                #Si la activiad no tiene hora de finalizacion se le asignara un valor nulo, que sera tratado
                #de una manera especial al insertarla,en otras palabras si la hora de finalizacion es nula
                #la duracion del turno estara determinada por el turno que empiece a la hora de inicio de 
                #dicha actividad
                if _end != None: # Actividad con Hora de finalizacion
                    _end= _end.split(':')
                    end_time = datetime.datetime(int(_date[0]) , int(_date[1]) , int (_date[2]),int(_end[0]), int(_end[1]))
                activity_list.append(Activity( date = datetime.datetime(int(_date[0]) , int(_date[1]) , int (_date[2]))  , 
                                           begin_time = datetime.datetime(int(_date[0]) , int(_date[1]) , int (_date[2]),int(_begin[0]), int(_begin[1])),
                                           end_time = end_time,name = _name)  )
    for x in activity_list: #primero se ubican las actividades que tienen hora inicio
        _day = x.date.isoweekday() - 1
        insert_activity(week[_day],x)
   
    for x in activity_list_no_begin: # insertar actividades que no tienen hora de inicio
        _date,_name = x
        
        _day = datetime.datetime(int(_date[0]),int(_date[1]),int(_date[2])).isoweekday() - 1

        for turn in range(0,len(week[_day])):#Recorrer todos los turnos del dia de la actividad sin inicio
            _begin,_end,_act = week[_day][turn]
            if _act.name == None:#Si el turn(i) no tiene alguna actividad asignada
                week[_day][turn] = (_begin,_end,Activity(_date,_begin,_end,_name))
                break
'''



def print_Activies(activity_list):
    for x in activity_list:
        print(f'{x.name} es el dia  {x.begin_time} y termina a las {x.end_time}')

def insert_activity(activity_list,new_activity):
    begin_time = new_activity.begin_time
    if new_activity.end_time == None:
        #Si el tiempo de finalizacion de una actividad es nulo(desconocido) , tampoco se conoce
        #la duracion
        duration = None
    else:
        #duracion es Tiempo de finalizacion - tiempo de Inicio
        duration = new_activity.end_time - new_activity.begin_time

    for i in range(0,len(activity_list)):
        #Recorrer todos las actividades(del dia especifico)
        current_begin_time,current_end_time,_ = activity_list[i]
        current_duration = current_end_time - current_begin_time

        if begin_time == current_begin_time:
            #si el tiempo de inicio de la actividad a insertar es = al del turno analizado en este momento

            if duration == None or duration == current_duration:
                #Si la actividad no tiene duracion o su duracion es = a la duracion del turno analizado en este momento
                activity_list[i] = (current_begin_time,current_end_time,new_activity)
                break

            elif duration < current_duration:
                #Si la duracion de la actividad es menor que la duracion del turno analizado en este momento
                if duration <= datetime.timedelta(minutes=30): 
                    #Si la duracion de la actividad es menor que 30 minutos
                    #Se crean dos nuevos turnos sobre el ya existente y se elimina el existente
                    
                    activity_list.insert(i,(current_begin_time + duration,current_end_time , Activity(None,None,None,None)) )
                    activity_list.insert(i,(current_begin_time,current_begin_time + duration ,new_activity) )
                    activity_list.pop(i+2)#Eleminar el turno existente
                    break
                    
                else:
                   activity_list[i] = (current_begin_time,current_begin_time + duration ,new_activity)
                   break 
            
            else:
                #Si la duracion de la actividad es mayor que la del turno en cuestion
                #Se crea un turno de Ininio de la actividad , Inicio de la actividad mas Duracion
                activity_list[i] = (begin_time,begin_time + duration ,new_activity)
                last_end = begin_time + duration

                for j in range(i+1,len(activity_list)):
                    #Recorrer los turnos restantes ese dia y dezplazarlos manteniendo sus duraciones pero alterando su hora de inicio
                    last_begin_time,last_end_time,curent_activity = activity_list[j]
                    activity_list[j] = (last_end , last_end + (last_end_time - last_begin_time ) , curent_activity)
                    last_end = last_end + (last_end_time - last_begin_time )

                break

        elif begin_time > current_begin_time and begin_time < current_end_time :
            #Si la actividad en custion comienza dentro del periodo de la duracion del turno en cuestion
            if new_activity.end_time == None or new_activity.end_time <= current_end_time :
                #Si no tiene duracion se le asigara una duracion de 30 minutos
                if new_activity.end_time == None :
                    duration = datetime.timedelta(minutes=30)

                if duration <= datetime.timedelta(minutes=30):
                    #Si la duracion de la actividad es menor igual que 30 minutos se crearan 2 turnos
                    #Uno vacio desde el inicio del turno hasta el inicio de la actividad
                    #Otro desde el comienzo de la actividad hasta su finalizacion
                    activity_list.insert(i,(begin_time,new_activity.end_time,new_activity) )
                    activity_list.insert(i,(current_begin_time ,current_begin_time + duration , Activity(None,None,None,None)) )
                    activity_list.pop(i+2)
                    break
                else : 
                    #En caso de que la duracion sea mayor que 30 mins solo se cambia el inicio y final del turno
                    activity_list[i] = (begin_time,begin_time + duration ,new_activity)
                    break 
            else :
                #Si la actividad termina despues de la hora de finalizacion del turno en cuestion
                #Se crea susutituye el turno desde el inicio de la actividad hasta inicio de la actividad + duracion
                activity_list[i] = (begin_time,begin_time + duration ,new_activity)
                last_end = begin_time + duration

                for j in range(i+1,len(activity_list)):
                    #Se desplazan el resto de las actividades
                    #Se mantienen su duracion solo se aplazan sus hora de inicio
                    last_begin_time,last_end_time,curent_activity = activity_list[j]
                    activity_list[j] = (last_end , last_end + (last_end_time - last_begin_time ) , curent_activity)
                    last_end = last_end + (last_end_time - last_begin_time )
                    

                break

    return activity_list

def clear_activity(activity_list,max_end_time):
    #Este metodo no lo utilice
    new_activity_list = []
    for x in activity_list :
        _,current_end_time,_ = x
        if current_end_time >= max_end_time:
            break
        new_activity_list.append(x)
    
    return new_activity_list

def print_activity_list(activity_list):
    #Este solo es para imprimir en consola
    for x in activity_list:
        begin, end ,activity = x
        print(f'{activity} begins at :  {begin}  and ends at : {end}' )
    print("#"*100)


class Activity:
    def __init__(self,date,begin_time,end_time,name):
        self.date = date
        self.begin_time = begin_time
        self.end_time = end_time
        self.name = name
    def __str__(self):
        return str(self.name)

vanilla_activity = Activity(None,None,None,None)


l1 = [ (datetime.datetime(2020,10,12,8),datetime.datetime(2020,10,12,9),vanilla_activity) , (datetime.datetime(2020,10,12,9),datetime.datetime(2020,10,12,10),vanilla_activity),
        (datetime.datetime(2020,10,12,10),datetime.datetime(2020,10,12,11),vanilla_activity),(datetime.datetime(2020,10,12,11),datetime.datetime(2020,10,12,12),vanilla_activity),
        (datetime.datetime(2020,10,12,12),datetime.datetime(2020,10,12,13),vanilla_activity),(datetime.datetime(2020,10,12,13),datetime.datetime(2020,10,12,14),vanilla_activity),
        (datetime.datetime(2020,10,12,14),datetime.datetime(2020,10,12,15),vanilla_activity),(datetime.datetime(2020,10,12,15),datetime.datetime(2020,10,12,16),vanilla_activity)]

l2 = [ (datetime.datetime(2020,10,13,8),datetime.datetime(2020,10,13,9),vanilla_activity) , (datetime.datetime(2020,10,13,9),datetime.datetime(2020,10,13,10),vanilla_activity),
        (datetime.datetime(2020,10,13,10),datetime.datetime(2020,10,13,11),vanilla_activity),(datetime.datetime(2020,10,13,11),datetime.datetime(2020,10,13,12),vanilla_activity),
        (datetime.datetime(2020,10,13,12),datetime.datetime(2020,10,13,13),vanilla_activity),(datetime.datetime(2020,10,13,13),datetime.datetime(2020,10,13,14),vanilla_activity),
        (datetime.datetime(2020,10,13,14),datetime.datetime(2020,10,13,15),vanilla_activity),(datetime.datetime(2020,10,13,15),datetime.datetime(2020,10,13,16),vanilla_activity)]

l3 = [ (datetime.datetime(2020,10,14,8),datetime.datetime(2020,10,14,9),vanilla_activity) , (datetime.datetime(2020,10,14,9),datetime.datetime(2020,10,14,10),vanilla_activity),
        (datetime.datetime(2020,10,14,10),datetime.datetime(2020,10,14,11),vanilla_activity),(datetime.datetime(2020,10,14,11),datetime.datetime(2020,10,14,12),vanilla_activity),
        (datetime.datetime(2020,10,14,12),datetime.datetime(2020,10,14,13),vanilla_activity),(datetime.datetime(2020,10,14,13),datetime.datetime(2020,10,14,14),vanilla_activity),
        (datetime.datetime(2020,10,14,14),datetime.datetime(2020,10,14,15),vanilla_activity),(datetime.datetime(2020,10,14,15),datetime.datetime(2020,10,14,16),vanilla_activity)]

l4 = [ (datetime.datetime(2020,10,15,8),datetime.datetime(2020,10,15,9),vanilla_activity) , (datetime.datetime(2020,10,15,9),datetime.datetime(2020,10,15,10),vanilla_activity),
        (datetime.datetime(2020,10,15,10),datetime.datetime(2020,10,15,11),vanilla_activity),(datetime.datetime(2020,10,15,11),datetime.datetime(2020,10,15,12),vanilla_activity),
        (datetime.datetime(2020,10,15,12),datetime.datetime(2020,10,15,13),vanilla_activity),(datetime.datetime(2020,10,15,13),datetime.datetime(2020,10,15,14),vanilla_activity),
        (datetime.datetime(2020,10,15,14),datetime.datetime(2020,10,15,15),vanilla_activity),(datetime.datetime(2020,10,15,15),datetime.datetime(2020,10,15,16),vanilla_activity)]

l5 = [ (datetime.datetime(2020,10,16,8),datetime.datetime(2020,10,16,9),vanilla_activity) , (datetime.datetime(2020,10,16,9),datetime.datetime(2020,10,16,10),vanilla_activity),
        (datetime.datetime(2020,10,16,10),datetime.datetime(2020,10,16,11),vanilla_activity),(datetime.datetime(2020,10,16,11),datetime.datetime(2020,10,16,12),vanilla_activity),
        (datetime.datetime(2020,10,16,12),datetime.datetime(2020,10,16,13),vanilla_activity),(datetime.datetime(2020,10,16,13),datetime.datetime(2020,10,16,14),vanilla_activity),
        (datetime.datetime(2020,10,16,14),datetime.datetime(2020,10,16,15),vanilla_activity),(datetime.datetime(2020,10,16,15),datetime.datetime(2020,10,16,16),vanilla_activity)]

l6 = [ (datetime.datetime(2020,10,17,8),datetime.datetime(2020,10,17,9),vanilla_activity) , (datetime.datetime(2020,10,17,9),datetime.datetime(2020,10,17,10),vanilla_activity),
        (datetime.datetime(2020,10,17,10),datetime.datetime(2020,10,17,11),vanilla_activity),(datetime.datetime(2020,10,17,11),datetime.datetime(2020,10,17,12),vanilla_activity),
        (datetime.datetime(2020,10,17,12),datetime.datetime(2020,10,17,13),vanilla_activity),(datetime.datetime(2020,10,17,13),datetime.datetime(2020,10,17,14),vanilla_activity),
        (datetime.datetime(2020,10,17,14),datetime.datetime(2020,10,17,15),vanilla_activity),(datetime.datetime(2020,10,17,15),datetime.datetime(2020,10,17,16),vanilla_activity)]

l7 = [ (datetime.datetime(2020,10,18,8),datetime.datetime(2020,10,18,9),vanilla_activity) , (datetime.datetime(2020,10,18,9),datetime.datetime(2020,10,18,10),vanilla_activity),
        (datetime.datetime(2020,10,18,10),datetime.datetime(2020,10,18,11),vanilla_activity),(datetime.datetime(2020,10,18,11),datetime.datetime(2020,10,18,12),vanilla_activity),
        (datetime.datetime(2020,10,18,12),datetime.datetime(2020,10,18,13),vanilla_activity),(datetime.datetime(2020,10,18,13),datetime.datetime(2020,10,18,14),vanilla_activity),
        (datetime.datetime(2020,10,18,14),datetime.datetime(2020,10,18,15),vanilla_activity),(datetime.datetime(2020,10,18,15),datetime.datetime(2020,10,18,16),vanilla_activity)]

L = [l1,l2,l3,l4,l5,l6,l7]


def getWeek():
    #return [l1,l2,l3,l4,l5]
    return [l1,l2,l3,l4,l5,l6,l7]

def getActivities():
    return []

def getFreeTurns(my_week):
    #free_Turns = [[],[],[],[],[]] 
    #real_free_Turns = [[],[],[],[],[]]
    free_Turns = [[],[],[],[],[] ,[],[]] #turnos libres
    real_free_Turns = [[],[],[],[],[],[],[]] #indices reales de los turnos
    for i in range(0,len(my_week)):
        z = 0
        for x in my_week[i]:
            _begin,_,_act = x
            if _act.name == None:
                free_Turns[i].append(_begin)
                real_free_Turns[i].append(z)
            z = z + 1
    return (free_Turns,real_free_Turns)

def printWeek(week):
    #Este metodo solo es para imprimir en consola
    print("Week after inserts")
    for x in week:
        print_activity_list(x)

def try_to_insert(free_Turns,activities,dayWeek,week,real_free_Turns):
    name,p,year,month,day,mj,actNumb,_ = activities[len(activities)-1] #actividad anadir
    i = dayWeek
    while True:
       #Recorrer todos los dias desde el dia que se quiere anadir
       #la actualizacion del dia esta abajo
       #estilo do while
        
        free_Turns_i = free_Turns[i] # obtener los turnos libres del dia i
        asigned_activities_i = []
        for x in activities:#Actividades asignadas al dia i
            _,_,_,_,_,_,_,_day = x

            if _day == i:
                asigned_activities_i.append(x)
        
        if len(asigned_activities_i) == len(free_Turns_i):
            #Ya esta lleno el dia indicado
            pass
        else:
            C = []
            for j in range(0,len(free_Turns_i)):
                C.append([])
            
            #Conformar la matriz de costos
            for x in asigned_activities_i:
                #Por cada actividad asignada en este dia tomar de su matriz de costos 
                # la fila asociada al dia en que se esta insertando la actividad
                _,_,_,_,_,_mj,_,_day = x
                for j in range(0,len(C)):
                    C[j].append(_mj[_day][j])

            for j in range(0,len(C)):
                #Anadir la columna de de costos de la actividad en custion que esta siendo insertada en este momento
                    C[j].append(mj[i][j])

            k = len(asigned_activities_i) + 1

            #metodo PULP
            #asign1 = runPulp(C)
            
            #Aqui iria real_asign = nodelp.solve "Libreria "
            
            
            #metodo Hungaro
            #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
            #no hace falta
            #hacer la matriz cuadrada
            for j in range(0,len(C)):
                for j1 in range(k,len(C)):
                    C[j].append(0)

           

           
            asign = hungarina_Alg(C)
            
            real_asign = []
            #obtener solo las asignaciones verdaderas
            for x in asign:
                r,c = x
                if c >= k:
                    continue
                real_asign.append(x)
            
            #]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
            
            #real_asign = runPulp(C)         


            #actualizar act
            activities[len(activities)-1] = (name,p,year,month,day,mj,actNumb,i)

            #limpiar la semana en ese dia
            for j in range(0,len(week[i])):
                _begin,_end,_act = week[i][j]
                if _begin in free_Turns_i:
                    week[i][j] = (_begin,_end,vanilla_activity)

            #asignar actividades
            k1 = 0#indice q ocupa la actividad q estoy insertando
            for j in range(0,len(asigned_activities_i)):
                _name,_p,_year,_month,_day,_,_,_ = asigned_activities_i[j]
                for x in real_asign: #buscar el turno al que fue asociado cada actividad
                    r,c = x
                    if c == j:
                        _begin,_end,_ = week[i][real_free_Turns[i][r]]
                        #buscar el turno que representa dicho turno realmente
                        week[i][real_free_Turns[i][r]] = (_begin,_end,Activity(datetime.datetime(_year,_month,_day),_begin,_end,_name))

                k1 = k1 + 1
            
            #asignar actividad en cuestion
            for x in real_asign:
                    r,c = x
                    if c == k1:
                        _begin,_end,_ = week[i][real_free_Turns[i][r]]
                        week[i][real_free_Turns[i][r]] = (_begin,_end,Activity(datetime.datetime(year,month,day),_begin,_end,name))
            
            break    
        
        

        i = i + 1
        if i == dayWeek:
            break
        elif i == 7:#5:
            i = 0

