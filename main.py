import sys
from dateutil.parser import parse
from datetime import datetime, timedelta
from src.services.order_service import OrderService
from src.database.DatabaseConnector import DatabaseConnector
from src.model.order import Order
from mongoengine import Q
from bson import DBRef, ObjectId

now_date = datetime.now()
db_connector = DatabaseConnector()
order_service = OrderService()

def main(schedule_at=None, enterprise_id="5e837a4a30fc256f5c3ad716"):
	
	try:
		print("Run application...")

		db_connector.connect_database()

		if schedule_at is None:
			schedule_at = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

		yesterday_start_date =	parse(schedule_at + " 00:00")
		yesterday_end_date 	 = 	parse(schedule_at + " 23:59")

		orders = Order.objects(
			deleted=False,
			enterprise=DBRef('enterprises', ObjectId(enterprise_id)),
		).filter(
			Q(scheduled_at__gte=yesterday_start_date) &
			Q(scheduled_at__lte=yesterday_end_date)
		)
	
		print("grouping OS by drivers...")
		orders_grouped = order_service.group_orders_by_driver(orders)

		for driver_id, driver_orders in orders_grouped.items():
      
			driver_orders_sorted = sorted(driver_orders, key=lambda x: x.start_time)
   
			working_day_realized = order_service.process_working_day_realized(driver_orders_sorted)
   
			working_day_foreseen = order_service.process_working_day_foreseen(driver_orders_sorted)
   
			driver = {
				"driver": driver_id,
				"working_day": {
					"realized": {
						"summary": working_day_realized['summary'],
						"details": working_day_realized['details']
     				},
					"foreseen": {
						"summary": working_day_foreseen['summary'],
						"details": working_day_foreseen['details']
     				}
				},
				"orders": list(map(lambda item: 
				item['id'], 
				driver_orders))
			}
			print(driver)
			print('\n\n\n')
			order_service.save_working_day(driver)

		print("Finish application...")
	except Exception as e:
		print(f'Error ocurred: {str(e)} on line {sys.exc_info()[-1].tb_lineno}')
		raise 

main()