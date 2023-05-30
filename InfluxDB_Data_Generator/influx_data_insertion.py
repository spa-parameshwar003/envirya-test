
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import datetime


token = "9ZZy-XrNu2weqaXne_SYG6BQBZWwNmWg_2z3ptBQZ2s6_h_1WVtPKoBS8PF5j_3dTGKsiVrgFuQPm4I9iwEI9A==" #update this variable with your secret token
org = "testorg"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="o2_data"

# start_date = int(datetime.datetime(2023, 4, 1, 0, 0).timestamp())
start_date = datetime.datetime(2023, 3, 3, 10, 30)

write_api = write_client.write_api(write_options=SYNCHRONOUS)
json_body = []

for value in range(50_00_000):
  sensor_id = random.randint(1, 1000)

  point = {
        "measurement": "o2_reading",
        "tags": {
            "sensor_name": "o2",
            "sensor_id": sensor_id,
            "data_type_of_sensor": "univariate" if sensor_id % 2 == 0 else "multivariate",
            "subsensor" : "o2"
        },
        "time": start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "fields": {
            "value": round(random.random() * random.randrange(1, 100),2),
            "units": "ppm"
        }
    }

  
  json_body.append(point)
  
  start_date = (start_date + datetime.timedelta(seconds=5))
  
  if value % 5000 == 0:
    write_api.write(bucket=bucket, org="testorg", record=json_body)
    print("batch completed ", value - 5000, value)
    json_body = []
    time.sleep(0.0001)
  
  
# query_api = write_client.query_api()

# query = """from(bucket: "o2_data")
#  |> range(start: -200d)
#  |> filter(fn: (r) => r._measurement == "o2_reading")"""
# tables = query_api.query(query, org="testorg")

# for table in tables:
#   for record in table.records:
#     print(record)
