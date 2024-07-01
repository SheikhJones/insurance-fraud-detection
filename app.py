import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, flash, send_file
from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import pickle

from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request

 

app = Flask(__name__) #Initialize the flask App

 
price = pickle.load(open('fraud.pkl','rb'))
@app.route('/')

@app.route('/index')
def index():
	return render_template('index.html')

 

#@app.route('/future')
#def future():
#	return render_template('future.html')    

@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/upload')
def upload():
    return render_template('upload.html')  
@app.route('/preview',methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html",df_view = df)	


 

@app.route('/prediction', methods = ['GET', 'POST'])
def prediction():
    return render_template('prediction.html')


#@app.route('/upload')
#def upload_file():
#   return render_template('BatchPredict.html')



@app.route('/predict', methods=['POST'])
def predict():
    try:
        int_features = [x for x in request.form.values()]
        print(int_features)
        int_features = [float(i) for i in int_features]
        final_features = [np.array(int_features)]
        prediction = price.predict(final_features)
        if prediction == 1:
            prediction_text = "Fraud"
        else:
            prediction_text = 'Non-fraud'
    except ValueError as e:
        # Handle the case where input values couldn't be converted to floats
        prediction_text = "Error: One or more input values are not valid"
    return render_template("prediction.html", prediction_text=prediction_text)

 
@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/performance')
def performance():
    return render_template('performance.html')

 
     
    
if __name__ == "__main__":
    app.run(debug=True)
