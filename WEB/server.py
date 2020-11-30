import traceback

from flask import Flask
from flask import render_template
from flask import request

from funcs import *
from BuildMj import buildMj



app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

myWeek = False
theWeek = None
canLoad = True
actNumb = 0
free_Turns = []
real_free_Turns = []
activities = []

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response



@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.form)
    if request.method == 'GET':
        return render_template('dashboard/index.html',week = myWeek,canLoad = canLoad)

@app.route('/home')
def about():
    return render_template('dashboard/index.html',week = myWeek,canLoad = canLoad)

@app.route('/today')
def today():
    if theWeek != None:
        _today = datetime.datetime.now()
        _year = _today.year
        _month = _today.month
        _day = _today.day
        i = 0
        while i < 7:
            _date ,_,_ = theWeek[i][0]
            if _date.year == _year and _date.month == _month and _date.day == _day:
                break
            i += 1
        if i == 7:
            return render_template('dashboard/day.html',day="Hoy",lista=[])
        else:
            activities = getDay(theWeek,i)
            webActivities = getWebDay(activities)
            return render_template('dashboard/day.html',day="Hoy",lista=webActivities)
    else:
        return render_template('dashboard/day.html',day="Hoy",lista=[])

@app.route('/monday')
def monday():
    if theWeek != None:
        activities = getDay(theWeek,0)
        webActivities = getWebDay(activities)
        
        return render_template('dashboard/day.html',day ="Lunes",lista = webActivities)
    return render_template('dashboard/day.html',day ="Lunes",lista = [])
@app.route('/tuesday')
def tuesday():
    if theWeek != None:
        activities = getDay(theWeek,1)
        webActivities = getWebDay(activities)
        return render_template('dashboard/day.html',day ="Martes",lista = webActivities)
    return render_template('dashboard/day.html',day ="Martes",lista = [])
@app.route('/wednesday')
def wednesday():
    if theWeek != None:
        activities = getDay(theWeek,2)
        webActivities = getWebDay(activities)
        return render_template('dashboard/day.html',day ="Miercoles",lista = webActivities)
    return render_template('dashboard/day.html',day ="Miercoles",lista = [])
@app.route('/thursday')
def thursday():
    if theWeek != None:
        activities = getDay(theWeek,3)
        webActivities = getWebDay(activities)
        return render_template('dashboard/day.html',day ="Jueves",lista = webActivities)
    return render_template('dashboard/day.html',day ="Jueves",lista = [])
@app.route('/friday')
def friday():
    if theWeek != None:
        activities = getDay(theWeek,4)
        webActivities = getWebDay(activities)
        return render_template('dashboard/day.html',day ="Viernes",lista = webActivities)
    return render_template('dashboard/day.html',day ="Viernes",lista = [])
@app.route('/saturday')
def saturday():
    if theWeek != None:
        activities = getDay(theWeek,5)
        webActivities = getWebDay(activities)
        return render_template('dashboard/day.html',day ="Sabado",lista = webActivities)
    return render_template('dashboard/day.html',day ="Sabado",lista = [])
@app.route('/sunday')
def sunday():
    if theWeek != None:
        activities = getDay(theWeek,6)
        webActivities = getWebDay(activities)
        return render_template('dashboard/day.html',day ="Domingo",lista = webActivities)
    return render_template('dashboard/day.html',day ="Domingo",lista = [])


@app.route('/webMakeWeek',methods=['GET', 'POST'])
def webMakeWeek():
    global myWeek
    global theWeek
    global free_Turns
    global real_free_Turns
    global activities
    print(request)
    print(request.form)
    a = request.form.get('makeWeekDate')
    print(a)
    theWeek = makeWeek(a)
    #printWeek(week)

    myWeek = True
    activities = []
    free_Turns, real_free_Turns = getFreeTurns(theWeek)
    return render_template('dashboard/index.html',week = myWeek, canLoad = canLoad)


@app.route('/webLoadFile',methods=['GET', 'POST'])
def webLoadFile():
    global theWeek
    global canLoad
    global free_Turns
    global real_free_Turns
    canLoad = False
    print(request)
    print(request.form)
    a = request.form.get('loadFile')
    print(a)
    loadFile(a,theWeek)
    printWeek(theWeek)
    free_Turns, real_free_Turns = getFreeTurns(theWeek)
    return render_template('dashboard/index.html',week = myWeek,canLoad = canLoad)

@app.route('/webResetWeek')
def webResetWeek():
    global theWeek
    global canLoad
    global free_Turns
    global real_free_Turns
    global activities
    canLoad = True

    theWeek = resetWeek(theWeek)
    free_Turns, real_free_Turns = getFreeTurns(theWeek)
    activities = []
    return render_template('dashboard/index.html',week = myWeek,canLoad = canLoad)


@app.route('/webExportWeek',methods = ['GET','POST'])
def webExportWeek():
    wN = request.form.get('weekName')
    exportWeek(theWeek,myWeek,canLoad,free_Turns,real_free_Turns,activities,actNumb,wN)
    return render_template('dashboard/index.html',week = myWeek,canLoad = canLoad)

@app.route('/webLoadWeek',methods = ['GET','POST'])
def webLoadWeek():
    global myWeek
    global theWeek 
    global canLoad 
    global actNumb 
    global free_Turns 
    global real_free_Turns 
    global activities 
    

    
    wN = request.form.get('loadWeek')
    theWeek,myWeek,canLoad,activities,actNumb,free_Turns,real_free_Turns = loadWeek(wN)
    return render_template('dashboard/index.html',week = myWeek,canLoad = canLoad)

@app.route('/webAddActivity', methods=['GET', 'POST'])
def webAddActivity():
    global theWeek
    global canLoad
    global actNumb
    global activities
    print(request)
    if request.method == 'GET':
        return render_template('dashboard/addActivity.html')
    else:
        canLoad = False
        print(request.form)
        aN = request.form.get('actName')
        aP = request.form.get('priority')
        aD = request.form.get('actDate')
        aD = aD.split('-')
        aH = request.form.get('hours')
        aM = request.form.get('minutes')

        insert_day = datetime.datetime(int(aD[0]),int(aD[1]),int(aD[2])).isoweekday() 


        #construir la matriz de costos asociados a una actividad
        mj = buildMj(int(aP),datetime.datetime(int(aD[0]),int(aD[1]),int(aD[2]),int(aH),int(aM)),insert_day,free_Turns)

        actNumb = actNumb + 1
        activities.append((aN,int(aP),int(aD[0]),int(aD[1]),int(aD[2]),mj,actNumb,-1))

        #anardir la actividad en la semana
        try_to_insert(free_Turns,activities,insert_day - 1,theWeek,real_free_Turns)

        return render_template('dashboard/index.html',week = myWeek,canLoad = canLoad)

if __name__ == '__main__':
    app.run(debug=True)