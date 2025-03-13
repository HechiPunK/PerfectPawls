
class Config:
    SECRET_KEY = 'JbYou03_mldnH9C4CQm61CMCsao'

class DevelopmentConfig(Config):  
    DEBUG = True
    MYSQL_HOST ='localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD =''
    MYSQL_DB ='inte'

config = {
    'development': DevelopmentConfig
}


