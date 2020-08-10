from flask import Flask
from flask_cors import CORS
from flask import request
from MusicPredictionFiles.scripts.PredictSongsNoGUI2 import Predictor
import time
app = Flask(__name__)
CORS(app)

@app.route('/get_grades', methods=['GET', 'POST'])
def get_grades(): 
    print("ressdfffff: ", type(request.files["file0"].filename))
    print("model arggg: ", request.args.get('model', ''))

    i = 0
    num_of_files = len(request.files)
    grades = dict()
    files_to_use = getFileNames(str(request.args.get('model','')))
    while i<num_of_files:
        file_name = "file"+str(i)
        file = request.files[file_name].read()
        prediction = Predictor()
        grade = prediction.predictSong(file, files_to_use[0],files_to_use[1], files_to_use[2], files_to_use[3],files_to_use[4],files_to_use[5])
        print("prediction: ", prediction)
        grades[request.files[file_name].filename] = grade
        i+=1


    return grades


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
    elif(index=="ABRSM_2019_2020(1-8)V3"):
        res = ["models/abrsm_2019_2020_all_3.sav", "data/abrsm_2019_2020_all_1.csv", 300,9,True,True]
    elif(index=="ABRSM_2020_2021(1-8)V1"):
        res = ["models/abrsm_2020_2021_all_1.sav", "data/abrsm_2020_2021_all_1.csv", 300,9,False,False]
    elif(index=="ABRSM_2020_2021(1-8)V2"):
        res = ["models/abrsm_2020_2021_all_2.sav", "data/abrsm_2020_2021_all_1.csv", 300,9,True,False]
    elif(index=="ABRSM_2020_2021(1-8)V3"):
        res = ["models/abrsm_2020_2021_all_3.sav", "data/abrsm_2020_2021_all_1.csv", 300,9,True,True]
    elif(index=="ABRSM_2019_2021(1-8)V1"):
        res = ["models/abrsm_2019_2021_all_1.sav", "data/abrsm_2019_2021_all_1.csv", 600,9,False,False]
    elif(index=="ABRSM_2019_2021(1-8)V2"):
        res = ["models/abrsm_2019_2021_all_2.sav", "data/abrsm_2019_2021_all_1.csv", 600,9,True,False]
    elif(index=="ABRSM_2019_2021(1-8)V3"):
        res = ["models/abrsm_2019_2021_all_3.sav", "data/abrsm_2019_2021_all_1.csv", 600,9,True,True]
    elif(index=="Piano Marvel(0-10)V1"):
        res = ["models/piano_marvel_all_2000_1.sav", "data/piano_marvel_all_2000_1.csv", 1000,9, False, False]
    elif(index=="Piano Marvel(0-10)V2"):
        res = ["models/piano_marvel_all_2000_2.sav", "data/piano_marvel_all_2000_1.csv", 1000,9,True,False]
    elif(index=="Piano Marvel(0-10)V3"):
        res = ["models/piano_marvel_all_2000_3.sav", "data/piano_marvel_all_2000_1.csv", 1000,9, True, True]
    else:
        res = ["models/abrsm_all_1.sav", "data/abrsm_all_1.csv", 300,9,False,False]

    
    return res

      
    