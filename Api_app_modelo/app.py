from flask import Flask, jsonify, request

from src.add_activity import addActivity
from src.single_add_activity import singleAddActivity
from src.funcs import loadFile,try_to_insert,getWeek,getFreeTurns,printWeek,getActivities, cleanWeek2

from utils.portals import convertActToListOfTuples, convertActToTuple
from utils.parse_act import parseAct

app = Flask(__name__)

my_week = getWeek()
# loadFile('activities.json', my_week)

free_Turns = []
real_free_Turns = []

# free_Turns, real_free_Turns = getFreeTurns(my_week)
activities = getActivities()

actNumb = 0

        
@app.route("/")
def index():

    return "Hello World!"

@app.route("/api/initialize")
def initialize():

    global my_week, free_Turns, real_free_Turns, activities

    free_Turns, real_free_Turns = getFreeTurns(my_week)
    activities = getActivities()

    return jsonify({"foo": "foo2"})    

@app.route("/api/load_file/")
def load_file():

    global my_week, free_Turns, real_free_Turns, activities

    loadFile('activities.json', my_week)    
    
    free_Turns, real_free_Turns = getFreeTurns(my_week)
    activities = getActivities()

    activities_result = parseAct(my_week)
    response = jsonify(activities_result)

    return response


@app.route("/api/delete_all_activities/")
def delete_all_activities():

    global my_week, free_Turns, real_free_Turns, activities, actNumb
    
    cleanWeek2(my_week)
    my_week = getWeek()
    # printWeek(my_week)
    free_Turns, real_free_Turns = getFreeTurns(my_week)
    activities = getActivities()
    actNumb = 0
    # loadFile('activities.json', my_week)

    return jsonify({"foo": "foo2"})


@app.route("/api/activities/", methods=["POST", "GET"])
def add_activity():

    global my_week, free_Turns, real_free_Turns, activities

    print("entró"+20*"#")
    activity = request.json
    entry_act = convertActToTuple(activity)
    # print("entry_act", entry_act)

    week_result = singleAddActivity(entry_act, my_week, free_Turns, real_free_Turns, activities, actNumb )

    activities_result = parseAct(week_result)
    print ("activities_result", activities_result)

    response = jsonify(activities_result)

    return response
    
    
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status_code": 404})


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"status_code": 500})

    

if __name__ == "__main__":
    # Debug mode is only for development mode.
    app.run(host = '0.0.0.0', debug=True)
