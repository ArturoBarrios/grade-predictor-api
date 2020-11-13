from flask import Flask
from flask_cors import CORS
from flask import request
from MusicPredictionFiles.scripts.PredictSongsNoGUI2 import Predictor
import time
import redis
import random
import json


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
r = redis.Redis(host='redis-10964.c89.us-east-1-3.ec2.cloud.redislabs.com', port=10964, password="0VY6S5d79kTkY5tlPjbfrM0Fk8vKdFjJ")

@app.route('/')
def default():
    return "Hello"

@app.route('/test')
def defaultTest():
    return "Hello Test"

@app.route('/get_grades', methods=['GET', 'POST'])
def get_grades(): 
    app.logger.info("testing info log")
    i = 0
    num_of_files = len(request.files)
    key = str(request.args.get('key',''))
    print("this is the fucking key: ", key)
    # grades = dict()
    grades = "{"
    files_to_use = getFileNames(str(request.args.get('model','')))
    while i<num_of_files:
        file_name = "file"+str(i)
        file = request.files[file_name].read()
        prediction = Predictor()
        grade = prediction.predictSong(file, files_to_use[0],files_to_use[1], files_to_use[2], files_to_use[3],files_to_use[4],files_to_use[5])
        # print("prediction: ", prediction)
        # grades[request.files[file_name].filename] = grade
        grades += "\""+request.files[file_name].filename+"\""+":"+"\""+str(grade)+"\""+","
        i+=1
    #remove comma
    grades = grades[0:len(grades)-1]
    grades += "}"

    
    #stringify grades object

    result = grades
    print("result of gradess: ", result) 
    print("typeof: ", type(grades))
    r.set(key,result)
    return key

@app.route('/get_grades_key', methods=['GET', 'POST'])
def getGradesKey():
    key = request.args.get("key")
    print("getting gradesssssss: ", key)
    grades = ""
    result = dict()
    try:
        print("in try")
        grades = r.get(str(key))
        print("grades: ", grades)
        result = json.loads(grades)
    except:
        result = dict()
    
    # print(grades)
    # app.logger.info("got grades: ", grades)

    return result

def getFileNames(index):
    res = None
    if(index=="ABRSM(1-8)V1"):
        res = ["models/abrsm_all_1.sav", "data/abrsm_all_1.csv", 500,9,False,False]
    elif(index=="ABRSM(1-8)V2"):
        res = ["models/abrsm_all_2.sav", "data/abrsm_all_1.csv", 300,9,True,False]
    elif(index=="ABRSM(1-8)V3"):
        res = ["models/abrsm_all_3.sav", "data/abrsm_all_1.csv", 300,9,True,True]
    elif(index=="ABRSM_2019_2020(1-8)V1"):
        res = ["models/abrsm_2019_2020_all_1.sav", "data/abrsm_2019_2020_all_1.csv", 300,9,False,False]
    elif(index=="ABRSM_2019_2020(1-8)V2"):
        res = ["models/abrsm_2019_2020_all_2.sav", "data/abrsm_2019_2020_all_1.csv", 300,9,True,False]
    # elif(index=="ABRSM_2019_2020(1-8)V3"):
    #     res = ["models/abrsm_2019_2020_all_3.sav", "data/abrsm_2019_2020_all_1.csv", 300,9,True,True]
    elif(index=="ABRSM_2020_2021(1-8)V1"):
        res = ["models/abrsm_2020_2021_all_1.sav", "data/abrsm_2020_2021_all_1.csv", 300,9,False,False]
    elif(index=="ABRSM_2020_2021(1-8)V2"):
        res = ["models/abrsm_2020_2021_all_2.sav", "data/abrsm_2020_2021_all_1.csv", 300,9,True,False]
    # elif(index=="ABRSM_2020_2021(1-8)V3"):
    #     res = ["models/abrsm_2020_2021_all_3.sav", "data/abrsm_2020_2021_all_1.csv", 300,9,True,True]
    elif(index=="ABRSM_2019_2021(1-8)V1"):
        res = ["models/abrsm_2019_2021_all_1.sav", "data/abrsm_2019_2021_all_1.csv", 600,9,False,False]
    elif(index=="ABRSM_2019_2021(1-8)V2"):
        res = ["models/abrsm_2019_2021_all_2.sav", "data/abrsm_2019_2021_all_1.csv", 600,9,True,False]
    # elif(index=="ABRSM_2019_2021(1-8)V3"):
    #     res = ["models/abrsm_2019_2021_all_3.sav", "data/abrsm_2019_2021_all_1.csv", 600,9,True,True]
    elif(index=="Piano Marvel(0-10)V1"):
        res = ["models/piano_marvel_all_2000_1.sav", "data/piano_marvel_all_2000_1.csv", 1000,9, False, False]
    elif(index=="Piano Marvel(0-10)V2"):
        res = ["models/piano_marvel_all_2000_2.sav", "data/piano_marvel_all_2000_1.csv", 1000,9,True,False]
    # elif(index=="Piano Marvel(0-10)V3"):
    #     res = ["models/piano_marvel_all_2000_3.sav", "data/piano_marvel_all_2000_1.csv", 1000,9, True, True]
    else:
        res = ["models/abrsm_all_1.sav", "data/abrsm_all_1.csv", 300,9,False,False]

    
    return res

      
if __name__ == "__main__":
    app.run(threaded=True)