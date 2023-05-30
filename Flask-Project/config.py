class Config(object):
    DEBUG = False
    TESTING = False
    TOKEN = "9ZZy-XrNu2weqaXne_SYG6BQBZWwNmWg_2z3ptBQZ2s6_h_1WVtPKoBS8PF5j_3dTGKsiVrgFuQPm4I9iwEI9A=="    
    INFLUX_ORG = "testorg"
    INFLUX_URL = "http://localhost:8086"

class Prod(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True