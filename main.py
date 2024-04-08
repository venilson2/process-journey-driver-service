import sys
from dateutil.parser import parse
from datetime import datetime, timedelta
from src.database.DatabaseConnector import DatabaseConnector
from src.model.order import Order
from mongoengine import Q
from bson import DBRef, ObjectId

now_date = datetime.now()
db_connector = DatabaseConnector()

def main(schedule_at=None, enterprise_id="5e837a4a30fc256f5c3ad716"):
	
	try:
		print("Run application...")

		db_connector.connect_database()

		if schedule_at is None:
			schedule_at = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

		yesterday_start_date = parse(schedule_at + " 00:00")
		yesterday_end_date = parse(schedule_at + " 23:59")

		orders = Order.objects(
			deleted=False,
			enterprise=DBRef('enterprises', ObjectId(enterprise_id)),
		).filter(
			Q(scheduled_at__gte=yesterday_start_date) &
			Q(scheduled_at__lte=yesterday_end_date)
		)
	
		print("grouping OS by drivers...")
		orders_grouped = group_orders_by_driver(orders)

		for driver_id, driver_orders in orders_grouped.items():
			driver_orders_sorted = sorted(driver_orders, key=lambda x: x.start_time)
			working_day = process_working_day(driver_orders_sorted)
   
			driver = {
				"driver": driver_id,
				"realized": working_day,
				# "orders": list(map(lambda item: item['id'], driver_orders))
			}
			print(driver)
			save_working_day(driver)

		print("Finish application...")
	except Exception as e:
		print(f'Error ocurred: {str(e)} on line {sys.exc_info()[-1].tb_lineno}')

def save_working_day(journey):
	print("Save journey...")
 
def process_working_day(driver_orders):
	work_time = 0
	unproductive_time = 0
	productive_time = 0
	on_hold = 0
	overtime = 0
	intra_day = 0
	inter_day = 0
 	
	for i in range(len(driver_orders) - 1): 
		current_order = driver_orders[i]
		next_order = driver_orders[i + 1]
     
		# Pegada - Inicio
		partial_duration_unproductive_time_init = calculate_hour_difference_from_iso_dates(
			current_order['started_improdutive_time_at'], 
			current_order['started_travel_at']
		)
		unproductive_time += partial_duration_unproductive_time_init

		# Finalizada - Largada
		partial_duration_unproductive_time_end = calculate_hour_difference_from_iso_dates(
			current_order['completed_at'], 
			current_order['delivered_at']
		)
		unproductive_time += partial_duration_unproductive_time_end
	
		# Inicio - Finalizada
		partial_duration_productive_time = calculate_hour_difference_from_iso_dates(
			current_order['started_travel_at'], 
			current_order['completed_at']
		)
		productive_time += partial_duration_productive_time

		# Pegada - Largada
		partial_duration_work_time = calculate_hour_difference_from_iso_dates(
			current_order['started_improdutive_time_at'], 
			current_order['delivered_at']
		)
		work_time += partial_duration_work_time

		# Se este não for o último pedido
		if i < len(driver_orders) - 1:
			partial_duration = calculate_hour_difference_from_iso_dates(
				next_order['started_improdutive_time_at'],
				current_order['delivered_at'], 
			)
			# 3600 - 60 minutos em segundos
			if partial_duration < 3600:
				on_hold += partial_duration
			else:
				intra_day += partial_duration
    
	return {
		"work_time": format_date(work_time),
		"unproductive_time": format_date(unproductive_time),
		"productive_time": format_date(productive_time),
		"on_hold": format_date(on_hold),
		"intra_day": format_date(intra_day),
	}
  
def group_orders_by_driver(orders):
	grouped_orders = {}
	for order in orders:
		driver_id = order.driver.id

		if driver_id not in grouped_orders:
			grouped_orders[driver_id] = []

		grouped_orders[driver_id].append(order)

	return grouped_orders

def calculate_hour_difference_from_iso_dates(start_date_iso, end_date_iso):
	
	if start_date_iso is None or end_date_iso is None:
		return 0

	time_difference = abs(end_date_iso - start_date_iso)
	
	return time_difference.total_seconds() / 3600

def format_date(hours):
    formatted_hours = int(hours)
    minutes = int((hours - formatted_hours) * 60)
    return f"{formatted_hours}:{minutes:02d}"

main("2024-04-05T00:00:00")