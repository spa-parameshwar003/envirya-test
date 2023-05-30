"""
Flask API for communicating with Influx DB

To Run: python3 run.py

API Description :
#################

Path : / , method = get
for checking API available or not

Path : getReadings/<rangeInput> , method = GET
for getting timeseries data for showing sensor readings in time series chart.

    parameters : rangeInput [Optional]

    response : [JSON]
        [
            {
                "result": "_result",
                "table": <table_value>,
                "type": <sensor_type>,
                "x": <timestamp1>,
                "y": <sensor_value>
            },
            {
                "result": "_result",
                "table": <table_value>,
                "type": <sensor_type>,
                "x": <timestamp2>,
                "y": <sensor_value>
            }
        ]

Path : getReadingsPagination , method = POST
for fetching data for infinite scrollable component

    request body : [JSON]
    {
        offset : <offset_value>,
        limit : <limit>
    }


    response : [JSON]
    [
        {
            "_field": "value",
            "_measurement": "o2_reading",
            "_start": "Sun, 28 May 2023 17:47:19 GMT",
            "_stop": "Mon, 29 May 2023 05:47:19 GMT",
            "_time": "Sun, 28 May 2023 17:47:20 GMT",
            "_value": 54.52,
            "data_type_of_sensor": "multivariate",
            "result": "_result",
            "sensor_id": "793",
            "sensor_name": "o2",
            "subsensor": "o2",
            "table": 0
        }
    ]

##################

"""
