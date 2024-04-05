from mongoengine import connect
from src.utils import ConfigPropertiesHelper

class DatabaseConnector:
    def __init__(self):
        self.cph = ConfigPropertiesHelper()

    def connect_database(self):
        MONGODB_ENVIRONMENT = self.cph.get_property_value('MONGODB', 'mongodb.environment')
        MONGODB_HOST 		= self.cph.get_property_value('MONGODB', f'mongodb.host.{MONGODB_ENVIRONMENT}')
        MONGODB_USER 		= self.cph.get_property_value('MONGODB', 'mongodb.user')
        MONGODB_PASS 		= self.cph.get_property_value('MONGODB', 'mongodb.pass')
        MONGODB_NAME 		= self.cph.get_property_value('MONGODB', f'mongodb.name.{MONGODB_ENVIRONMENT}')
        
        if MONGODB_HOST == 'localhost':
            connect(MONGODB_NAME)
        else:
            dbqs = 'mongodb+srv://{db_user}:{db_pass}@{db_host}/{db_name}?retryWrites=true&w=majority'.format(
                db_host=MONGODB_HOST,
                db_user=MONGODB_USER,
                db_pass=MONGODB_PASS,
                db_name=MONGODB_NAME
            )

            connect(host=dbqs)
