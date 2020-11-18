from flask import Flask
from flask_cors import CORS
from flask import request
from MusicPredictionFiles.scripts.PredictSongsNoGUI2 import Predictor
import time
import redis
import random
import json
from rq import Queue
from rq.job import Job
from worker import conn


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
r = redis.Redis(host='redis-19075.c74.us-east-1-4.ec2.cloud.redislabs.com', port=19075, password="jPzU5Mm1rynGQJ3WQEwRgjiiy26WsKNx")

q = Queue(connection=conn)

@app.route('/')
def default():
    return "Hello"
#key, count, model, model, model, model, model, file, filename
@app.route('/test',methods=['GET', 'POST'])
def defaultTest():
    print("test called")
    url = "test"
    #
    num_of_files = len(request.files)
   
    i = 0
    arr = []
    files_to_use = getFileNames(str(request.args.get('model','')))
    key = str(request.args.get('key',''))
    arr.append(str(request.args.get('key','')))
    arr.append(num_of_files)
    arr.append(files_to_use[0])
    arr.append(files_to_use[1])
    arr.append(str(files_to_use[2]))
    arr.append(str(files_to_use[3]))
    arr.append(files_to_use[4])
    arr.append(files_to_use[5])
    while i<num_of_files:
        file_name = "file"+str(i)
        file = request.files[file_name].read()
        actual_file_name = request.files[file_name].filename
        arr.append(file)
        arr.append(actual_file_name)
        
        i+=1

    job = q.enqueue_call(
            func=get_grades, args=(arr,), result_ttl=5000
        )
    return key
    

def test_function_params(url):
    print("test function params called array: ", url)
    return "test function params returned"


# @app.route('/get_grades', methods=['GET', 'POST'])
def get_grades(arr): 
    i = 0
    j = 0
    num_of_files = arr[1]
    key = arr[0]
    print("this is the  key: ", key)
    print("this is more text!!!")
    print("this is the  key: ", key)
    print("this is more text!!!")
    print("this is the  key: ", key)
    print("this is more text!!!")
    # grades = dict()
    grades = "{"
    # files_to_use = arr[1]
    arr_of_names_and_songs = arr[8:]
    while j<num_of_files:
        # file_name = "file"+str(i)
        file = arr_of_names_and_songs[i] #request.files[file_name].read()
        prediction = Predictor()
        print("bool values:     ",arr[6], "    ", arr[7])
        grade = prediction.predictSong(file, arr[2],arr[3], 300, 9,arr[6],arr[7])
        # print("prediction: ", prediction)
        # grades[request.files[file_name].filename] = grade
        grades += "\""+arr_of_names_and_songs[i+1]+"\""+":"+"\""+str(grade)+"\""+","
        i+=2
        j+=1
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
#comment
      
if __name__ == "__main__":
    app.run()