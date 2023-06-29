import flask
import sqlite3
import json
from flask import render_template
from frontend import result


app = flask.Flask(__name__)
app.config["DEBUG"] = True

if not result:
        print("No data was returned")
train_list = result[0]
      
@app.route('/api/v1', methods=['GET'])
def home():
    return '''<h1> API Data Page </h1>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/train/result', methods=['GET'])
def api_filter():
    
    for i in range(1,len(train_list)):
        dictionary_key = train_list[i]
        start_station = dictionary_key['start_station']
        destination = dictionary_key['destination']

        query1 = "SELECT DISTANCE FROM TRAIN_DETAILS WHERE"
        query2 = "SELECT TRAIN_NAME FROM TRAIN_DETAILS WHERE"

        if start_station:
            query1 += ' START_STATION = "' + start_station + '" AND '
            query2 += ' START_STATION = "' + start_station + '" AND '
        if destination:
            query1 += ' DESTINATION = "' + destination + '";'
            query2 += ' DESTINATION = "' + destination + '";'
        if not (start_station or destination):
            return page_not_found(404)

        connection = sqlite3.connect('train.db')
        current = connection.cursor()
    
        result1 = current.execute(query1).fetchall()
        result2 = current.execute(query2).fetchall()
        
        jsonString1 = json.dumps(result1)
        jsonString2 = json.dumps(result2)
        
        tempjsonString1 = jsonString1.replace('[[','')
        finaljsonString1 = tempjsonString1.replace(']]', '')
    
        tempjsonString2 = jsonString2.replace('[[','')
        finaljsonString2 = tempjsonString2.replace(']]', '')
        
    final_result = [{'first_value': finaljsonString1, 'second_value': finaljsonString2}]
    
    return render_template('result.html', jsonString=final_result)
    
def start():
    app.run(debug = False, port = 8000)

start()   
    

