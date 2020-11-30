import datetime


def buildMj(Act_p, Act_hI,Act_D,FreeTurns):
    #Crear Matriz de costos para una actividad dada
    Des = [0,1,3,5,7,9,11,13,15,17]
    Mj = []

    for x in FreeTurns: #Crear una matriz de costos del mismo tamano que freeTruns
        a = [0] * len(x)
        Mj.append(a)
    
    #Los valores en la matriz yo los guardaba en minutos y no en horas para evitar valores con coma
    for i in range(0,len(FreeTurns)):
        j = i + 1 # j esta idexado en base 1 ya que los dias son de 1...7
        for k in range(0,len(FreeTurns[i])):
            if j < Act_D :
                #todos los turnos de dias anteriores al de la actividad seran penalizados
                Mj[i][k] = 1100 * 60#600
            elif j == Act_D:
                #si el dia de la actividad en cuestion coincide con el turno
                #Act_hi : Hora de inicio de la actividad
                #FreeTurns[i][j] : Hora de Ininico del turno j el dia i
                Mj[i][k] = Act_p + (abs(Act_hI-FreeTurns[i][k]).seconds / 60 ) * Des[Act_p]
            else:
                #Si el turno es un dia j , posterior al dia de la actividad
                #FreeTurns[i][0] : Hora de Ininico del turno 0 el dia i
                Mj[i][k] = Act_p +  ( ( (FreeTurns[i][k] - FreeTurns[i][0]).seconds / 60) + (9 * 60 * (j - Act_D))) * Des[Act_p + j - Act_D]


    return Mj 

T = [[8,9,10,11,12],[8,9,10,11,12],[8,9,10,11,12],[8,9,10,11,12],[8,9,10,11,12]]
T1=[
    [datetime.datetime(2020,10,12,8),datetime.datetime(2020,10,12,9),datetime.datetime(2020,10,12,10),datetime.datetime(2020,10,12,11),datetime.datetime(2020,10,12,12)]
    ,[datetime.datetime(2020,10,13,8),datetime.datetime(2020,10,13,9),datetime.datetime(2020,10,13,10),datetime.datetime(2020,10,13,11),datetime.datetime(2020,10,13,12)]
    ,[datetime.datetime(2020,10,14,8),datetime.datetime(2020,10,14,9),datetime.datetime(2020,10,14,10),datetime.datetime(2020,10,14,11),datetime.datetime(2020,10,14,12)]
    ,[datetime.datetime(2020,10,15,8),datetime.datetime(2020,10,15,9),datetime.datetime(2020,10,15,10),datetime.datetime(2020,10,15,11),datetime.datetime(2020,10,15,12)]
    ,[datetime.datetime(2020,10,16,8),datetime.datetime(2020,10,16,9),datetime.datetime(2020,10,16,10),datetime.datetime(2020,10,16,11),datetime.datetime(2020,10,16,16)]]

#[(datetime.datetime(2020,10,17,8),(datetime.datetime(2020,10,17,9),(datetime.datetime(2020,10,17,10),(datetime.datetime(2020,10,17,11),(datetime.datetime(2020,10,17,12)]

#print(buildMj(2,10,3,T))


#print(buildMj(2,datetime.datetime(2020,10,12,18),1,T1))

#print( ((datetime.datetime(2020,10,17,10,30) - datetime.datetime(2020,10,17,8)).seconds) / 60 / 60) 