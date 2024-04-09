from src.utils import DateTimeUtils

class OrderService:

	def __init__(self):
		self.date_utils = DateTimeUtils()

	def save_working_day(self, working_day):
		print("Save working_day...")
 
	def process_working_day(self, driver_orders):
		work_time = 0
		unproductive_time = 0
		productive_time = 0
		on_hold_time = 0
		overtime = 0
		intra_day = 0
		inter_day = 0
  
		orders = []
		
		for i in range(len(driver_orders) - 1): 
			current_order = driver_orders[i]
			next_order = driver_orders[i + 1]
		
			# Pegada - Inicio
			partial_duration_unproductive_time_init = self.date_utils.calculate_hour_difference_from_iso_dates(
				current_order['started_improdutive_time_at'], 
				current_order['started_travel_at']
			)
			unproductive_time += partial_duration_unproductive_time_init

			# Finalizada - Largada
			partial_duration_unproductive_time_end = self.date_utils.calculate_hour_difference_from_iso_dates(
				current_order['completed_at'], 
				current_order['delivered_at']
			)
			unproductive_time += partial_duration_unproductive_time_end
		
			# Inicio - Finalizada
			partial_duration_productive_time = self.date_utils.calculate_hour_difference_from_iso_dates(
				current_order['started_travel_at'], 
				current_order['completed_at']
			)
			productive_time += partial_duration_productive_time

			# Pegada - Largada
			partial_duration_work_time = self.date_utils.calculate_hour_difference_from_iso_dates(
				current_order['started_improdutive_time_at'], 
				current_order['delivered_at']
			)
			work_time += partial_duration_work_time

			# Se este não for o último pedido
			if i < len(driver_orders) - 1:
				partial_duration = self.date_utils.calculate_hour_difference_from_iso_dates(
					next_order['started_improdutive_time_at'],
					current_order['delivered_at'], 
				)
	
				if partial_duration < 60:
					on_hold_time += partial_duration
				else:
					intra_day += partial_duration
     
			orders.append({
				"id": current_order['id'],
				"intra_day": self.date_utils.convert_minute_in_hours(partial_duration),
				"started_improdutive_time_at": current_order['started_improdutive_time_at'],
				"started_travel_at": current_order['started_travel_at'],
				"completed_at": current_order['completed_at'],
				"delivered_at": current_order['delivered_at'],
				"unproductive_time_init": self.date_utils.convert_minute_in_hours(partial_duration_unproductive_time_init),
				"unproductive_time_end": self.date_utils.convert_minute_in_hours(partial_duration_unproductive_time_end),
				"productive_time": self.date_utils.convert_minute_in_hours(partial_duration_productive_time),
				"work_time": self.date_utils.convert_minute_in_hours(partial_duration_work_time),
				"on_hold_time": self.date_utils.convert_minute_in_hours(partial_duration),
				"overtime": self.date_utils.convert_minute_in_hours(partial_duration),
				"intra_day": self.date_utils.convert_minute_in_hours(partial_duration),
			})
		
		summary = {
			"work_time": self.date_utils.convert_minute_in_hours(work_time),
			"unproductive_time": self.date_utils.convert_minute_in_hours(unproductive_time),
			"productive_time": self.date_utils.convert_minute_in_hours(productive_time),
			"on_hold_time": self.date_utils.convert_minute_in_hours(on_hold_time),
			"intra_day": self.date_utils.convert_minute_in_hours(intra_day),
			"inter_day": self.date_utils.convert_minute_in_hours(inter_day),
			"overtime": self.date_utils.convert_minute_in_hours(overtime),
		}
  
		return {
			"summary": summary,
			"orders": orders
		}
  
	def group_orders_by_driver(self, orders):
		grouped_orders = {}
		for order in orders:
			driver_id = order.driver.id

			if driver_id not in grouped_orders:
				grouped_orders[driver_id] = []

			grouped_orders[driver_id].append(order)

		return grouped_orders 