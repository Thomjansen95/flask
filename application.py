from flask import Flask, render_template, jsonify, request
import flask
import boto3
import logging
import json

application = Flask(__name__)
app = application
# Index route
@app.route('/')
def index():
    return render_template('index.html')

client = boto3.client('lambda',
    region_name = "eu-central-1"
)
                        
@app.route("/", methods=['GET', 'POST'])
@app.route("/calculate_heartrate_range", methods=['GET', 'POST'])
def calculate_heartrate_range():
    "Endpoint for calculating the heart rate range"
    if request.method == 'GET':
        #return the form
        return render_template('sample_lambda.html')
    if request.method == 'POST':
        #return the range        
        age = int(request.form.get('age'))        
        payload = {"age":age} 
        #Invoke a lambda function which calculates the max heart rate and gives the target heart rate range              
        result = client.invoke(FunctionName="FlaskTestLambda",
                    InvocationType='RequestResponse',                                      
                    Payload=json.dumps(payload))
        range = result['Payload'].read()      
        api_response = json.loads(range)               
        return jsonify(api_response)      

if __name__ == '__main__':
    app.run(debug=True)