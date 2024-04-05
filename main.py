import sys
from dateutil.parser import parse
from datetime import datetime, timedelta
from src.database.DatabaseConnector import DatabaseConnector
from src.model.order import Order
from mongoengine import Q
from bson import DBRef, ObjectId

now_date = datetime.now()
db_connector = DatabaseConnector()

def main(schedule_at=now_date, enterprise_id="5e837a4a30fc256f5c3ad716"):
	print("Run application...")
	try:
		db_connector.connect_database()
  
		yesterday_start_date = parse((schedule_at - timedelta(days=1)).strftime("%Y-%m-%d") + " 00:00")
		yesterday_end_date = parse((schedule_at - timedelta(days=1)).strftime("%Y-%m-%d") + " 23:59")
  
		orders = Order.objects(
					deleted=False,
					enterprise=DBRef('enterprises', ObjectId(enterprise_id))
				).filter(
					Q(scheduled_at__gte=yesterday_start_date) &
					Q(scheduled_at__lte=yesterday_end_date)
				);
		print("Finish application...")
	except Exception as e:
		print(f'Error ocurred: {str(e)} on line {sys.exc_info()[-1].tb_lineno}')

def save_journey():
	print("Save journey...")
main()