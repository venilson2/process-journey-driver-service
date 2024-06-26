import configparser
from datetime import datetime

class ConfigPropertiesHelper(object):
	config = None
	
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read('config.properties')
	
	def get_property_value(self, section, property):
		return self.config.get(section, property)

class DateTimeUtils:
    
    def __init__(self):
        pass
    
    def calculate_hour_difference_from_iso_dates(self, start_date_iso, end_date_iso):
        if start_date_iso is None or end_date_iso is None:
            return 0
        
        time_difference = abs(end_date_iso - start_date_iso)
        duration_in_seconds = time_difference.total_seconds()
        duration_in_minutes = duration_in_seconds / 60
        return duration_in_minutes
    
    def convert_minute_in_hours(self, minutes):
        hours = minutes // 60
        minutes_remaining = minutes % 60
        return f"{int(hours):02d}:{int(minutes_remaining):02d}"
    
    
    def calculate_hour_difference(self, hour_start_str, hour_end_str):
        
        if hour_start_str is None or hour_end_str is None:
            return 0
        
        hour_start = datetime.strptime(hour_start_str, "%H:%M")
        hour_end = datetime.strptime(hour_end_str, "%H:%M")

        hour_diff = hour_end - hour_start

        hours_in_minutes = (hour_diff.seconds // 60) % 60

        return hours_in_minutes