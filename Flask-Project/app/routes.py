from app import app
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from config import Prod
from flask import jsonify, request
from flask_cors import CORS
import datetime


cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

bucket = "my-bucket"

client = InfluxDBClient(url=Prod.INFLUX_URL, token=Prod.TOKEN, org=Prod.INFLUX_ORG)

query_api = client.query_api()


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/getReadings/')
@app.route('/getReadings/<rangeInput>')
def getReadings(rangeInput=None):
    print(rangeInput)
    if rangeInput:
        startTime = datetime.datetime.utcnow() - datetime.timedelta(minutes=int(rangeInput))
        timeRangeStart = startTime.strftime('%Y-%m-%dT%H:%M:%SZ')
        timeRangeStop = (startTime +  datetime.timedelta(minutes=int(rangeInput))).strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        startTime = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
        timeRangeStart = startTime.strftime('%Y-%m-%dT%H:%M:%SZ')
        timeRangeStop = (startTime +  datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%SZ')
    print("time ", timeRangeStart, timeRangeStop)
    
    # |> range(start: {timeRangeStart}, stop: {timeRangeStop}) 
    # |> range(start: -5m)
    
    try:
        tables = query_api.query(f"""from(bucket:"o2_data")
                                |> range(start: {timeRangeStart}, stop: {timeRangeStop}) 
                                |> filter(fn: (r) => r["_measurement"] == "o2_reading" and r["_field"] == "value")
                                |> sort(columns: ["_time"], desc: true)
                                |> map(fn: (r) => ({{x: r._time,y: r._value,type: r.data_type_of_sensor}}))
                                |> group(columns: ["x"])
                                """)
    
        result = []
        for table in tables:
            for row in table.records:
                result.append(row.values)
        return jsonify(result)
    except Exception as e:
        return f"Something went wroong! {e}", 500
    

@app.route('/getReadingsPagination/', methods=["POST"])
def getReadingsPagination():
    inputData = request.get_json()
    offset = inputData["offset"]
    limit = inputData["limit"]
    
    try:
        tables = query_api.query(f"""from(bucket:"o2_data")
                                |> range(start: -12h) 
                                |> filter(fn: (r) => r["_measurement"] == "o2_reading" and r["_field"] == "value")
                                |> sort(columns: ["_time"], desc: true)
                                |> group(columns: ["_time"])
                                """)
    
        result = []
        for table in tables:
            for row in table.records:
                result.append(row.values)
        return jsonify(result[ offset : offset+limit])
    except Exception as e:
        return f"Something went wroong! {e}", 500