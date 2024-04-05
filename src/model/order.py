# -*- coding: utf-8 -*-
import datetime, logging
from bson import json_util, ObjectId
from mongoengine import *
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, EmbeddedDocumentListField, FloatField, IntField, ReferenceField, StringField, ListField, MultiPointField

ENTERPRISE_WORK_FORMATS = ('lines', 'routes')
USER_PROFILES = ('master', 'admin', 'traffic-control', 'driver', 'engineer', 'customer', 'passenger')
DIRECTION_OPTIONS = ('incoming', 'outcoming', 'both', 'circular')
POINT_CATEGORIES = ('passenger','parking')
FIELD_TYPES = ('string', 'double', 'integer', 'currency', 'phone', 'text', 'date', 'datetime', 'file', 'options')
WAYPOINT_STATUS = ('pending', 'partial', 'total', 'skipped')
PASSENGER_STATUS = ('pending', 'shipped', 'skipped')
REPAIR_REQUEST_STATUS = ('pending', 'in_progress', 'done', 'canceled', 'wontfix')
REPAIR_REQUEST_PRIORITY = ('low', 'average', 'high')
EVENT_TYPES = ('speed_over_limit', 'fence_scape')
GPS_UPDATE_FONTS = ('vehicle-tracker', 'driver-app', 'passenger-app')
COURSES = ('orders', 'repair_request', 'fuel_supply_record', 'checklist_vehicle', 'checklist_sanitary')
CREDENTIAL_CARD_TYPE = ('aba-track','serial','wiegand','decimal')

'''
' Configurations
'''
class CustomQuerySet(QuerySet):
	def to_json(self, explode_data=True):
		return "[%s]" % (",".join([doc.to_json(explode_data) for doc in self]))
	def to_json_all(self):
		return "[%s]" % (",".join([doc.to_json_all() for doc in self]))

class CustomBaseDocument(Document):
	# default configurations
	meta = {'queryset_class': CustomQuerySet, 'abstract': True}
	
	# default fields
	created_at 			= DateTimeField(default=datetime.datetime.now)
	updated_at 			= DateTimeField()
	user_update 		= ReferenceField('User')
	deleted 			= BooleanField(default=False)
	deleted_at 			= DateTimeField()
	user_delete 		= ReferenceField('User')
	wrong_location 		= BooleanField(default=False)
	active 				= BooleanField(default=True)
	inactive_at 		= DateTimeField()

	def set_all_values(self, data):
		for attr in data:
			if hasattr(self, attr):
				setattr(self, attr, data[attr])

'''
' EmbeddedDocuments
'''

class RatingItem(EmbeddedDocument):
	name = StringField()
	description = StringField()
	level = IntField(default=0)
	
class Attachment(EmbeddedDocument):
	name = StringField()
	size = StringField()
	extension = StringField()
	path = StringField()
	description = StringField()
	uploaded_at = DateTimeField(default=datetime.datetime.now)

class ActivityTime(EmbeddedDocument):
	start_time = StringField()
	end_time = StringField()

class VehicleRoute(EmbeddedDocument):
	vehicle 		= ReferenceField('Vehicle')
	activity_times 	= EmbeddedDocumentListField(ActivityTime)

class Schedule(EmbeddedDocument):
	departure_time 	= StringField()
	vehicle = ReferenceField('Vehicle')

class WaypointPassenger(EmbeddedDocument):
	passenger = ReferenceField('Passenger')
	status = StringField(choices=PASSENGER_STATUS, default='pending')
	comments = StringField()
	updated_at = DateTimeField()

class WaypointRoute(EmbeddedDocument):
	point = ReferenceField('Point')
	
	incoming_time = StringField()
	incoming_distance = FloatField()
	incoming_duration = FloatField()

	outcoming_time = StringField()
	outcoming_distance = FloatField()
	outcoming_duration = FloatField()
	
	passengers = EmbeddedDocumentListField(WaypointPassenger)
	status = StringField(choices=WAYPOINT_STATUS, default='pending')
	comments = StringField()
	scheduled_at = DateTimeField()
	executed_at = DateTimeField()
	vehicle_tracker_passed = BooleanField(default=False)
	vehicle_tracker_passed_time = IntField() # Seconds
	vehicle_tracker_passed_distance = IntField() # Meters

class EventDataRecord(EmbeddedDocument):
	key = StringField()
	value = DynamicField()

class RouteWorkCalendar(EmbeddedDocument):
	work_calendar = ReferenceField('WorkCalendar')
	work_shift = StringField()
	arrival_time_incoming = StringField()
	arrival_time_outcoming = StringField()
	additional_time_type = StringField()
	additional_time_type_waypoints = IntField()
	waypoints = EmbeddedDocumentListField(WaypointRoute)

class VehicleSeat(EmbeddedDocument):
	name = StringField()
	is_hall = BooleanField(default=False)
	is_void = BooleanField(default=False)
	is_driver = BooleanField(default=False)
	passenger = ReferenceField('Passenger')

class VehicleSeatsRow(EmbeddedDocument):
	seats = EmbeddedDocumentListField(VehicleSeat)
	
class RoutePassengersSeatsLayout(EmbeddedDocument):
	oid = ObjectId()
	description = StringField()
	vehicle_type = StringField()
	positions = EmbeddedDocumentListField(VehicleSeatsRow)

class CheckListItemOption(EmbeddedDocument):
	value = StringField()
	selected = BooleanField(default=False)
	color = StringField()

class CheckListItem(EmbeddedDocument):
	question = StringField()
	description = StringField()
	response = DynamicField()
	response_type = StringField(choices=FIELD_TYPES)
	response_options = EmbeddedDocumentListField(CheckListItemOption)
	comments = StringField()
	attachments = EmbeddedDocumentListField(Attachment)

class Course(EmbeddedDocument):
	name = StringField(choices=COURSES)
	is_done = BooleanField(default=False)
	completed_at = DateTimeField(default=datetime.datetime.now)

class LineRoute(EmbeddedDocument):
	route = ReferenceField('Route')
	direction = StringField(choices=DIRECTION_OPTIONS)

class Coordinates(EmbeddedDocument):
	latitude = FloatField()
	longitude = FloatField()

class AddressInfo(EmbeddedDocument):
	label = StringField()
	zip_code = StringField()
	street = StringField()
	house_number = StringField()
	complement = StringField()
	district = StringField()
	state = StringField()
	city = StringField()
	country = StringField()
	postal_code = StringField()
	location = PointField()

class VehicleTypeCostItem(EmbeddedDocument):
	value = FloatField()
	cost_item = ReferenceField('VehicleCostItem')

class TransportOverviewSummaryPublicOptions(EmbeddedDocument):
	name = StringField()
	color = StringField()
	icon = StringField()

class TransportOverviewSummaryPublic(EmbeddedDocument):
	options = EmbeddedDocumentListField(TransportOverviewSummaryPublicOptions)

class TransportOverviewSummaryWalking(EmbeddedDocument):
	time = StringField()

class TransportOverviewSummary(EmbeddedDocument):
	walking = EmbeddedDocumentField(TransportOverviewSummaryWalking)
	public = EmbeddedDocumentField(TransportOverviewSummaryPublic)

class TransportOverviewPrice(EmbeddedDocument):
	amount = StringField()
	currency = StringField()
	summary = StringField()

class TransportTime(EmbeddedDocument):
	startInMin = IntField()
	start = StringField()
	end = StringField()
	durationInMin = IntField()
	duration = IntField()

class TransportOverview(EmbeddedDocument):
	time = EmbeddedDocumentField(TransportTime)
	price = EmbeddedDocumentField(TransportOverviewPrice)
	type = StringField()
	summary = EmbeddedDocumentListField(TransportOverviewSummary)

class TransportDetailsLocation(EmbeddedDocument):
	start = StringField()
	end = StringField()

class TransportDetailsSegmentsMainStops(EmbeddedDocument):
	color = StringField()
	icon = StringField()
	name = StringField()
	location = PointField()
	type = StringField()

class TransportDetailsSegmentsMainSchedule(EmbeddedDocument):
	transportName = StringField()
	transportType = StringField()
	icon = StringField()
	color = StringField()

class TransportDetailsSegmentsMain(EmbeddedDocument):
	stops = EmbeddedDocumentListField(TransportDetailsSegmentsMainStops)
	schedule = EmbeddedDocumentField(TransportDetailsSegmentsMainSchedule)

class TransportDetailsSegmentsPublic(EmbeddedDocument):
	time = EmbeddedDocumentField(TransportTime)
	main = EmbeddedDocumentField(TransportDetailsSegmentsMain)

class TransportDetailsSegmentsWalking(EmbeddedDocument):
	location = EmbeddedDocumentField(TransportDetailsLocation)
	distance = IntField()
	time = EmbeddedDocumentField(TransportTime)
	main = EmbeddedDocumentField(TransportDetailsSegmentsMain)

class TransportDetailsSegments(EmbeddedDocument):
	walking = EmbeddedDocumentField(TransportDetailsSegmentsWalking)
	public = EmbeddedDocumentField(TransportDetailsSegmentsPublic)

class TransportDetails(EmbeddedDocument):
	location = EmbeddedDocumentField(TransportDetailsLocation)
	segments = EmbeddedDocumentListField(TransportDetailsSegments)

class Transport(EmbeddedDocument):
	routeId 	= StringField()
	overview 	= EmbeddedDocumentField(TransportOverview)
	details 	= EmbeddedDocumentField(TransportDetails)

class TimeSlot(EmbeddedDocument):
	description = StringField()
	start_time 	= StringField()
	end_time 	= StringField()
	driver		= ReferenceField('User')
	vehicle		= ReferenceField('Vehicle')

class TripPerformed(EmbeddedDocument):
	boarding_point 		= ReferenceField('Point')
	passengers_boarded 	= ListField(ReferenceField('Passenger'))
	executed_at 		= DateTimeField(default=datetime.datetime.now)
	
'''
' Documents
'''
class Configuration(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'configurations'}

	# Collection fields
	key = StringField(required=True)
	value = DynamicField(required=True)
	enterprise = ReferenceField('Enterprise')

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None

		return json_util.dumps(data)

class Enterprise(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'enterprises'}

	# Collection fields
	name = StringField()
	use_access_control = BooleanField(default=False)
	use_app_mobile = BooleanField(default=False)
	use_app_driver = BooleanField(default=False)
	use_speed_control = BooleanField(default=False)
	work_format = StringField(choices=ENTERPRISE_WORK_FORMATS)
	getrak_id =	IntField()

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None

		return json_util.dumps(data)

class User(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'users'}

	# Collection fields
	name = StringField(required=True)
	full_name = StringField()
	login = StringField(required=True)
	password = DynamicField()
	profile = StringField(required=True, choices=USER_PROFILES)
	enterprise = ReferenceField('Enterprise')
	subenterprise = ReferenceField('SubEnterprise')
	subenterprises = ListField(ReferenceField('SubEnterprise'))
	cpf = StringField()
	enrollment = StringField()
	address = StringField()
	personal_phone_number = StringField()
	company_phone_number = StringField()
	cnh_number = StringField()
	cnh_due_date = DateTimeField()
	cnh_front_path = StringField()
	cnh_back_path = StringField()
	change_password = BooleanField(default=True)
	avatar_path = StringField()
	last_vehicle_driven = ReferenceField('Vehicle')
	courses = EmbeddedDocumentListField(Course)
	verified = BooleanField(default=False)
	passenger = ReferenceField('Passenger')
	validation_code = IntField()
	admission_at = DateTimeField()
	resignation_at = DateTimeField()
	app_last_login_version = StringField()
	

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		if not (self.password is None):
			del data['password']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None
		data["cnh_due_date"] = data["cnh_due_date"].strftime("%d/%m/%Y") if "cnh_due_date" in data else None
		data["inactive_at"] = data["inactive_at"].strftime("%d/%m/%Y") if "inactive_at" in data else None
		data["admission_at"] 	= data["admission_at"].strftime("%d/%m/%Y") if "admission_at" in data else None
		data["resignation_at"] 	= data["resignation_at"].strftime("%d/%m/%Y") if "resignation_at" in data else None

		if not (self.subenterprises is None):
			data['subenterprises'] = []

			for subenterprise in self.subenterprises:
				obj = subenterprise.to_mongo()
				obj["id"] = str(subenterprise.id)
				del obj['_id']

				data['subenterprises'].append(obj)

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']
		
		if not (self.passenger is None):
			data['passenger'] = self.passenger.to_mongo()
			data['passenger']["id"] = str(self.passenger.id)
			del data['passenger']['_id']

			if not (self.passenger.subenterprise is None):
				data['passenger']['subenterprise'] = self.passenger.subenterprise.to_mongo()
				data['passenger']['subenterprise']["id"] = str(self.passenger.subenterprise.id)
				del data['passenger']['subenterprise']['_id']
		
		if not (self.subenterprise is None):
			data['subenterprise'] = self.subenterprise.to_mongo()
			data['subenterprise']["id"] = str(self.subenterprise.id)
			del data['subenterprise']['_id']

		if not (self.last_vehicle_driven is None):
			data['last_vehicle_driven'] = self.last_vehicle_driven.to_mongo()
			data['last_vehicle_driven']["id"] = str(self.last_vehicle_driven.id)
			del data['last_vehicle_driven']['_id']

		return json_util.dumps(data)

class UserLog(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'user_logs'}

	# Collection fields
	user = ReferenceField('User')
	app_version = StringField()
	ip = StringField()
	location = PointField()

class Point(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'points'}

	# Collection fields
	category = StringField(choices=POINT_CATEGORIES)
	description = StringField()
	location = PointField()
	enterprise = ReferenceField('Enterprise')

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None

		if self.wrong_location == True:
			data['location']['latitude'] = data['location']['coordinates'][0]
			data['location']['longitude'] = data['location']['coordinates'][1]
		else:
			data['location']['latitude'] = data['location']['coordinates'][1]
			data['location']['longitude'] = data['location']['coordinates'][0]

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None

		return json_util.dumps(data)

class Route(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'routes'}

	# Collection fields
	hexcode 		= StringField()
	description 	= StringField()
	color 			= StringField()
	direction 		= StringField(choices=DIRECTION_OPTIONS, default='both')
	vehicles 		= EmbeddedDocumentListField(VehicleRoute)
	schedule_grid 	= EmbeddedDocumentListField(Schedule)
	work_calendars 	= EmbeddedDocumentListField(RouteWorkCalendar)
	enterprise 		= ReferenceField('Enterprise')
	subenterprise 	= ReferenceField('SubEnterprise')
	seats_layouts 	= EmbeddedDocumentListField(RoutePassengersSeatsLayout)
	customized 		= BooleanField(default=False)
	customized_by 	= ReferenceField('User')
	time_slots		= EmbeddedDocumentListField(TimeSlot)
	path 			= MultiPointField()

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["updated_at"] = data["updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "updated_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None
		data["inactive_at"] = data["inactive_at"].strftime("%d/%m/%Y") if "inactive_at" in data else None

		if explode_data and not (self.work_calendars is None):
			data['work_calendars'] = []

			for wc in self.work_calendars:
				obj = wc.to_mongo()
				
				obj['work_calendar'] = wc.work_calendar.to_mongo()
				obj['work_calendar']["id"] = str(wc.work_calendar.id)
				del obj['work_calendar']['_id']

				obj['waypoints'] = []
				for wr in wc.waypoints:
					wp = wr.to_mongo()
					
					wp['point'] = wr.point.to_mongo()
					wp['point']["id"] = str(wr.point.id)
					del wp['point']['_id']

					if wr.point.wrong_location == True:
						wp['point']['location']['latitude'] = wp['point']['location']['coordinates'][0]
						wp['point']['location']['longitude'] = wp['point']['location']['coordinates'][1]
					else:
						wp['point']['location']['latitude'] = wp['point']['location']['coordinates'][1]
						wp['point']['location']['longitude'] = wp['point']['location']['coordinates'][0]
					
					wp['point']["created_at"] = wp['point']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in wp['point'] else None
					wp['point']["deleted_at"] = wp['point']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in wp['point'] else None

					if not (wr.passengers is None) and len(wr.passengers) > 0:
						wp['passengers'] = []
						
						for passenger in wr.passengers:
							ps = passenger.to_mongo()

							ps['passenger'] = passenger.passenger.to_mongo()
							ps['passenger']["id"] = str(passenger.passenger.id)
							del ps['passenger']['_id']

							ps['passenger']["created_at"] = ps['passenger']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in ps['passenger'] else None
							ps['passenger']["deleted_at"] = ps['passenger']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in ps['passenger'] else None
							
							# del ps['passenger']['routes']
							# ps['passenger']['routes'] = []
							# for route in passenger.passenger.routes:
							# 	rte = route.to_mongo()
							# 	rte["id"] = str(route.id)
							# 	del rte['_id']

							# 	if rte["enterprise"]:
							# 		rte['enterprise'] = route.enterprise.to_mongo()
							# 		rte['enterprise']["id"] = str(route.enterprise.id)
							# 		del rte['enterprise']['_id']

							# 	if rte["subenterprise"]:
							# 		rte['subenterprise'] = route.subenterprise.to_mongo()
							# 		rte['subenterprise']["id"] = str(route.subenterprise.id)
							# 		del rte["subenterprise"]['_id']

							# 	### Removendo para ficar mais leve
							# 	if rte["seats_layouts"]:
							# 		del rte["seats_layouts"]

							# 	if rte["work_calendars"]:
							# 		del rte["work_calendars"]

							# 	if rte["vehicles"]:
							# 		del rte["vehicles"]

							# 	if rte["schedule_grid"]:
							# 		del rte["schedule_grid"]

							# 	ps['passenger']['routes'].append(rte)
							
							wp['passengers'].append(ps)

					obj['waypoints'].append(wp)
				data['work_calendars'].append(obj)				
		elif not (self.work_calendars is None):
			del data['work_calendars']

		if not (self.seats_layouts is None):
			data['seats_layouts'] = []
			for sl in self.seats_layouts:
				vl = sl.to_mongo()
				
				vl['positions'] = []
				for row in sl.positions:
					r = row.to_mongo()
					
					r['seats'] = []
					for seat in row.seats:
						s = seat.to_mongo()

						if not (seat.passenger is None):
							s['passenger'] = seat.passenger.to_mongo()
							s['passenger']["id"] = str(seat.passenger.id)
							del s['passenger']['_id']

							s['passenger']["created_at"] = s['passenger']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in s['passenger'] else None
							s['passenger']["deleted_at"] = s['passenger']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in s['passenger'] else None

						r['seats'].append(s)
					
					vl['positions'].append(r)

				data['seats_layouts'].append(vl)

		if explode_data and not (self.vehicles is None):
			data['vehicles'] = []

			for vh in self.vehicles:
				obj = vh.to_mongo()
				
				obj['vehicle'] = vh.vehicle.to_mongo()
				obj['vehicle']["id"] = str(vh.vehicle.id)
				del obj['vehicle']['_id']

				obj['vehicle']["created_at"] = obj['vehicle']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in obj['vehicle'] else None
				obj['vehicle']["updated_at"] = obj['vehicle']["updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "updated_at" in obj['vehicle'] else None
				obj['vehicle']["deleted_at"] = obj['vehicle']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in obj['vehicle'] else None
				obj['vehicle']["gps_updated_at"] = obj['vehicle']["gps_updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "gps_updated_at" in obj['vehicle'] else None

				if not(vh.vehicle.location is None) and not(vh.vehicle.location == False):
					if vh.vehicle.wrong_location == True:
						obj['vehicle']['location']['latitude'] = obj['vehicle']['location']['coordinates'][0]
						obj['vehicle']['location']['longitude'] = obj['vehicle']['location']['coordinates'][1]
					else:
						obj['vehicle']['location']['latitude'] = obj['vehicle']['location']['coordinates'][1]
						obj['vehicle']['location']['longitude'] = obj['vehicle']['location']['coordinates'][0]

				if not (vh.vehicle.line is None):
					obj['vehicle']['line'] = vh.vehicle.line.to_mongo()
					obj['vehicle']['line']["id"] = str(vh.vehicle.line.id)
					del obj['vehicle']['line']['_id']

				data['vehicles'].append(obj)
		elif not (self.vehicles is None):
			del data['vehicles']

		if explode_data and not (self.schedule_grid is None):
			data['schedule_grid'] = []

			for sg in self.schedule_grid:
				obj = sg.to_mongo()
				
				obj['vehicle'] = sg.vehicle.to_mongo()
				obj['vehicle']["id"] = str(sg.vehicle.id)
				del obj['vehicle']['_id']

				obj['vehicle']["created_at"] = obj['vehicle']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in obj['vehicle'] else None
				obj['vehicle']["deleted_at"] = obj['vehicle']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in obj['vehicle'] else None

				if not(sg.vehicle.location is None) and not(sg.vehicle.location == False):
					if sg.vehicle.wrong_location == True:
						obj['vehicle']['location']['latitude'] = obj['vehicle']['location']['coordinates'][0]
						obj['vehicle']['location']['longitude'] = obj['vehicle']['location']['coordinates'][1]
					else:
						obj['vehicle']['location']['latitude'] = obj['vehicle']['location']['coordinates'][1]
						obj['vehicle']['location']['longitude'] = obj['vehicle']['location']['coordinates'][0]

				if not (sg.vehicle.line is None):
					obj['vehicle']['line'] = sg.vehicle.line.to_mongo()
					obj['vehicle']['line']["id"] = str(sg.vehicle.line.id)
					del obj['vehicle']['line']['_id']

				data['schedule_grid'].append(obj)
		elif not (self.schedule_grid is None):
			del data['schedule_grid']

		if explode_data and not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None
		elif not (self.enterprise is None):
			del data['enterprise']
		
		if not (self.subenterprise is None):
			data['subenterprise'] = self.subenterprise.to_mongo()
			data['subenterprise']["id"] = str(self.subenterprise.id)
			del data['subenterprise']['_id']

			data['subenterprise']["created_at"] = data['subenterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['subenterprise'] else None
			data['subenterprise']["deleted_at"] = data['subenterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['subenterprise'] else None
		
		if not (self.customized_by is None):
			data['customized_by'] = self.customized_by.to_mongo()
			data['customized_by']["id"] = str(self.customized_by.id)
			del data['customized_by']['_id']
		
		if not (self.path is None):
			data['path'] = []
			for coord in self.path['coordinates']:
				data['path'].append({
					'latitude': coord[1],
					'longitude': coord[0]
				})

		return json_util.dumps(data)

class SubEnterprise(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'subenterprises'}

	# Collection fields
	name = StringField()
	hexcode = StringField()
	enterprise = ReferenceField('Enterprise')
	use_temperature_control = BooleanField(default=False)
	credential_card_type = StringField(choices=CREDENTIAL_CARD_TYPE)

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"]  = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"]  = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None
		data["inactive_at"] = data["inactive_at"].strftime("%d/%m/%Y") if "inactive_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None

		return json_util.dumps(data)

class Line(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'lines'}

	# Collection fields
	description = StringField()
	enterprise = ReferenceField('Enterprise')
	subenterprise = ReferenceField('SubEnterprise')
	routes = EmbeddedDocumentListField(LineRoute)

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None
		
		if not (self.subenterprise is None):
			data['subenterprise'] = self.subenterprise.to_mongo()
			data['subenterprise']["id"] = str(self.subenterprise.id)
			del data['subenterprise']['_id']

			data['subenterprise']["created_at"] = data['subenterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['subenterprise'] else None
			data['subenterprise']["deleted_at"] = data['subenterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['subenterprise'] else None	

		if not (self.routes is None):
			data['routes'] = []

			for lr in self.routes:
				obj = lr.to_mongo()
				
				obj['route'] = lr.route.to_mongo()
				obj['route']["id"] = str(lr.route.id)
				del obj['route']['_id']

				if not (lr.route.subenterprise is None):
					obj['route']['subenterprise'] = lr.route.subenterprise.to_mongo()
					obj['route']['subenterprise']["id"] = str(lr.route.subenterprise.id)
					del obj['route']['subenterprise']['_id']


				if not(lr.route.work_calendars is None):
					obj['route']['work_calendars'] = []

					for wc in lr.route.work_calendars:
						_obj = wc.to_mongo()
						
						_obj['work_calendar'] = wc.work_calendar.to_mongo()
						_obj['work_calendar']["id"] = str(wc.work_calendar.id)
						del _obj['work_calendar']['_id']

						_obj['waypoints'] = []
						for wr in wc.waypoints:
							wp = wr.to_mongo()
							
							wp['point'] = wr.point.to_mongo()
							wp['point']["id"] = str(wr.point.id)
							del wp['point']['_id']

							if wr.point.wrong_location == True:
								wp['point']['location']['latitude'] = wp['point']['location']['coordinates'][0]
								wp['point']['location']['longitude'] = wp['point']['location']['coordinates'][1]
							else:
								wp['point']['location']['latitude'] = wp['point']['location']['coordinates'][1]
								wp['point']['location']['longitude'] = wp['point']['location']['coordinates'][0]
							
							wp['point']["created_at"] = wp['point']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in wp['point'] else None
							wp['point']["deleted_at"] = wp['point']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in wp['point'] else None

							if not (wr.passengers is None) and len(wr.passengers) > 0:
								wp['passengers'] = []
								
								for passenger in wr.passengers:
									ps = passenger.to_mongo()

									ps['passenger'] = passenger.passenger.to_mongo()
									ps['passenger']["id"] = str(passenger.passenger.id)
									del ps['passenger']['_id']
									del ps['passenger']['routes']
									del ps['passenger']['enterprise']
									del ps['passenger']['subenterprises']

									wp['passengers'].append(ps)

							_obj['waypoints'].append(wp)
						
						obj['route']['work_calendars'].append(_obj)

				data['routes'].append(obj)

		return json_util.dumps(data)

class VehicleCheckListHistory(CustomBaseDocument):
	meta = {'collection': 'vehicle_checklist_histories'}

	enterprise = ReferenceField('Enterprise')
	vehicle = ReferenceField('Vehicle')
	driver = ReferenceField('User')
	items = EmbeddedDocumentListField(CheckListItem)

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] 			= data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] 		 	= data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None
		data["updated_at"] 		 	= data["updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "updated_at" in data else None
		
		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None
		
		if not (self.vehicle is None):
			data['vehicle'] = self.vehicle.to_mongo()
			data['vehicle']["id"] = str(self.vehicle.id)
			del data['vehicle']['_id']

			data['vehicle']["created_at"] = data['vehicle']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['vehicle'] else None
			data['vehicle']["deleted_at"] = data['vehicle']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['vehicle'] else None

		if not (self.driver is None):
			data['driver'] = self.driver.to_mongo()
			data['driver']["id"] = str(self.driver.id)
			del data['driver']['_id']

			data['driver']["created_at"] = data['driver']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['driver'] else None
			data['driver']["deleted_at"] = data['driver']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['driver'] else None

		return json_util.dumps(data)
	
class VehicleLayout(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'vehicle_layouts'}
	
	# Collection fields
	description = StringField()
	positions = EmbeddedDocumentListField(VehicleSeatsRow)
	vehicle_type = StringField()
	enterprise = ReferenceField('Enterprise')

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] 			= data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] 		 	= data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None
		data["updated_at"] 		 	= data["updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "updated_at" in data else None
		
		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None

		return json_util.dumps(data)

class Vehicle(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'vehicles'}

	# Collection fields
	plate = StringField()
	description = StringField()
	line = ReferenceField('Line')
	route = ReferenceField('Route')
	active_order = ReferenceField('Order')
	icon = StringField()
	getrak_id = IntField()
	is_online = BooleanField(default=False)
	speed = IntField()
	location = PointField()
	enterprise = ReferenceField('Enterprise')
	gps_updated_at = DateTimeField()
	gps_update_font = StringField(default='vehicle-tracker', choices=GPS_UPDATE_FONTS)
	fuel_tank_size = FloatField()
	odometer_value = FloatField()
	odometer_value_last_fuel_supply = FloatField()
	autonomy_average = FloatField()
	fuel_avaliable_stock = FloatField()
	fuel_stocked_at = DateTimeField()
	seats_layout = ReferenceField('VehicleLayout')
	purchased_at = DateTimeField()
	sold_at = DateTimeField()
	vehicle_rfid = ReferenceField('Vehicle')
	vehicle_jammer = ReferenceField('Vehicle')
	alert_days_expiration_artesp 	= IntField(default=10)
	alert_days_expiration_mip 		= IntField(default=10)
	alert_days_expiration_dtp  		= IntField(default=10)
	alert_days_expiration_emtu 		= IntField(default=10)
	expiration_artesp_at			= DateTimeField()
	expiration_mip_at				= DateTimeField()
	expiration_dtp_at				= DateTimeField()
	expiration_emtu_at				= DateTimeField()
	
	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] 				= data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] 		 		= data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None
		data["updated_at"] 		 		= data["updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "updated_at" in data else None
		data["gps_updated_at"] 	    	= data["gps_updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "gps_updated_at" in data else None
		data["fuel_stocked_at"]     	= data["fuel_stocked_at"].strftime("%d/%m/%Y %H:%M:%S") if "fuel_stocked_at" in data else None
		data["purchased_at"]        	= data["purchased_at"].strftime("%d/%m/%Y") if "purchased_at" in data else None
		data["sold_at"]             	= data["sold_at"].strftime("%d/%m/%Y") if "sold_at" in data else None
		data["inactive_at"] 			= data["inactive_at"].strftime("%d/%m/%Y") if "inactive_at" in data else None
		data["expiration_artesp_at"] 	= data["expiration_artesp_at"].strftime("%d/%m/%Y") if "expiration_artesp_at" in data else None
		data["expiration_mip_at"] 		= data["expiration_mip_at"].strftime("%d/%m/%Y") if "expiration_mip_at" in data else None
		data["expiration_dtp_at"] 		= data["expiration_dtp_at"].strftime("%d/%m/%Y") if "expiration_dtp_at" in data else None
		data["expiration_emtu_at"] 		= data["expiration_emtu_at"].strftime("%d/%m/%Y") if "expiration_emtu_at" in data else None

		if (self.location == False) or (self.location is None):
			if 'location' in data:
				del data['location']
		else:
			if self.wrong_location == True:
				data['location']['latitude'] = data['location']['coordinates'][0]
				data['location']['longitude'] = data['location']['coordinates'][1]
			else:
				data['location']['latitude'] = data['location']['coordinates'][1]
				data['location']['longitude'] = data['location']['coordinates'][0]

		if not (self.line is None):
			data['line'] = self.line.to_mongo()
			data['line']["id"] = str(self.line.id)
			del data['line']['_id']
		
		if not (self.route is None):
			data['route'] = self.route.to_mongo()
			data['route']["id"] = str(self.route.id)
			del data['route']['_id']
		
		# if not (self.active_order is None):
		# 	try:
		# 		data['active_order'] = self.active_order.to_mongo()
		# 		data['active_order']["id"] = str(self.active_order.id)
		# 		del data['active_order']['_id']

		# 		if not (self.active_order.route is None):
		# 			data['active_order']['route'] = json_util.loads(self.active_order.route.to_json())
		# 			# data['active_order']['route']["id"] = str(self.active_order.route.id)
		# 			# del data['active_order']['route']['_id']

		# 			if not (self.active_order.route.work_calendars is None):
		# 				del data['active_order']['route']['work_calendars']

		# 			if not (self.active_order.route.seats_layouts is None):
		# 				del data['active_order']['route']['seats_layouts']

		# 			if not (self.active_order.route.subenterprise is None):
		# 				data['active_order']['route']['subenterprise'] = self.active_order.route.subenterprise.to_mongo()
		# 				data['active_order']['route']['subenterprise']["id"] = str(self.active_order.route.subenterprise.id)
		# 				del data['active_order']['route']['subenterprise']['_id']
				
		# 		if not (self.active_order.driver is None):
		# 			data['active_order']['driver'] = self.active_order.driver.to_mongo()
		# 			data['active_order']['driver']["id"] = str(self.active_order.driver.id)
		# 			del data['active_order']['driver']['_id']
				
		# 		aux = {
		# 			'id': data['active_order']["id"],
		# 			'route': data['active_order']['route'],
		# 			'driver': data['active_order']['driver']
		# 		}

		# 		del data['active_order']

		# 		data['active_order'] = aux
		# 	except Exception as e:
		# 		logging.error(e)
		# 		pass
		
		if not (self.seats_layout is None):
			data['seats_layout'] = self.seats_layout.to_mongo()
			data['seats_layout']["id"] = str(self.seats_layout.id)
			del data['seats_layout']['_id']

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None
		
		if not (self.vehicle_rfid is None):
			data['vehicle_rfid'] = self.vehicle_rfid.to_mongo()
			data['vehicle_rfid']["id"] = str(self.vehicle_rfid.id)
			del data['vehicle_rfid']['_id']

		if not (self.vehicle_jammer is None):
			data['vehicle_jammer'] = self.vehicle_jammer.to_mongo()
			data['vehicle_jammer']["id"] = str(self.vehicle_jammer.id)
			del data['vehicle_jammer']['_id']
   
		data['alert_days_expiration_artesp'] 	= self.alert_days_expiration_artesp
		data['alert_days_expiration_mip'] 		= self.alert_days_expiration_mip
		data['alert_days_expiration_dtp'] 		= self.alert_days_expiration_dtp
		data['alert_days_expiration_emtu'] 		= self.alert_days_expiration_emtu

		return json_util.dumps(data)

class Passenger(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'passengers'}

	# Collection fields
	name = StringField()
	cpf = StringField()
	personal_phone_number = StringField()
	enrollment = StringField()
	credential = StringField()
	credential_card_type = StringField(choices=CREDENTIAL_CARD_TYPE)
	credential_aba_track_code = StringField()
	credential_serial_code = StringField()
	credential_wiegand_code = StringField()
	admission_at = DateTimeField()
	resignation_at = DateTimeField()
	enterprise = ReferenceField('Enterprise')
	subenterprise = ReferenceField('SubEnterprise')
	subenterprises = ListField(ReferenceField('SubEnterprise'))
	line = ReferenceField('Line')
	route = ReferenceField('Route')
	routes = ListField(ReferenceField('Route'))
	address = EmbeddedDocumentField(AddressInfo)
	transport = StringField()

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] 		= data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] 		= data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None
		data["admission_at"] 	= data["admission_at"].strftime("%d/%m/%Y") if "admission_at" in data else None
		data["resignation_at"] 	= data["resignation_at"].strftime("%d/%m/%Y") if "resignation_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']
		
		if not (self.subenterprises is None):
			data['subenterprises'] = []

			for subenterprise in self.subenterprises:
				obj = subenterprise.to_mongo()
				obj["id"] = str(subenterprise.id)
				del obj['_id']

				data['subenterprises'].append(obj)

		if not (self.routes is None):
			data['routes'] = []

			for route in self.routes:
				obj = route.to_mongo()
				obj["id"] = str(route.id)
				del obj['_id']

				# if not (route.enterprise is None):
				# 	obj['enterprise'] = route.enterprise.to_mongo()
				# 	obj['enterprise']["id"] = str(route.enterprise.id)
				# 	del obj['enterprise']['_id']

				# if not (route.subenterprise is None):
				# 	obj['subenterprise'] = route.subenterprise.to_mongo()
				# 	obj['subenterprise']["id"] = str(route.subenterprise.id)
				# 	del obj['subenterprise']['_id']

				# ### Removendo para ficar mais leve
				# if route.seats_layouts:
				# 	del obj['seats_layouts']

				# if route.work_calendars:
				# 	del obj['work_calendars']

				# if route.vehicles:
				# 	del obj['vehicles']

				# if route.schedule_grid:
				# 	del obj['schedule_grid']

				data['routes'].append(obj)

		if not (self.subenterprise is None):
			data['subenterprise'] = self.subenterprise.to_mongo()
			data['subenterprise']["id"] = str(self.subenterprise.id)
			del data['subenterprise']['_id']

		if not (self.line is None):
			data['line'] = self.line.to_mongo()
			data['line']["id"] = str(self.line.id)
			del data['line']['_id']

		if not (self.route is None):
			data['route'] = self.route.to_mongo()
			data['route']["id"] = str(self.route.id)
			del data['route']['_id']		

		return json_util.dumps(data)

class IgnitionControl(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'ignition_control'}

	vehicle = ReferenceField('Vehicle')
	device_id = StringField()
	is_logged = BooleanField(default=True)
	is_active = BooleanField(default=True)
	send_enabled = BooleanField(default=True)

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] 		= data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] 		= data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None

		if not (self.vehicle is None):
			data['vehicle'] = self.vehicle.to_mongo()
			data['vehicle']["id"] = str(self.vehicle.id)
			del data['vehicle']['_id']

			data['vehicle']["created_at"] = data['vehicle']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['vehicle'] else None
			data['vehicle']["deleted_at"] = data['vehicle']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['vehicle'] else None
			data['vehicle']["gps_updated_at"] = data['vehicle']["gps_updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "gps_updated_at" in data['vehicle'] else None

			if not (self.vehicle.enterprise is None):
				data['vehicle']['enterprise'] = self.vehicle.enterprise.to_mongo()
				data['vehicle']['enterprise']["id"] = str(self.vehicle.enterprise.id)
				del data['vehicle']['enterprise']['_id']

				data['vehicle']['enterprise']["created_at"] = data['vehicle']['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['vehicle']['enterprise'] else None
				data['vehicle']['enterprise']["deleted_at"] = data['vehicle']['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['vehicle']['enterprise'] else None

		return json_util.dumps(data)

class Checkin(CustomBaseDocument):
	# Collection configuration
	meta = {'collection': 'checkins'}

	# Collection fields
	enterprise = ReferenceField('Enterprise')
	
	order = ReferenceField('Order')
	checkin_point = ReferenceField('Point')

	vehicle = ReferenceField('Vehicle')
	passenger = ReferenceField('Passenger')
	credential = StringField()
	line = ReferenceField('Line')
	route = ReferenceField('Route')
	location = PointField()
	temperature = FloatField()
	registered_at = DateTimeField()
	source = StringField(default='vehicle-tracker', choices=GPS_UPDATE_FONTS)

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["registered_at"] 	= data["registered_at"].strftime("%d/%m/%Y %H:%M:%S") if "registered_at" in data else None
		data["created_at"] 		= data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] 		= data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None

		if not (self.location is None):
			if self.wrong_location == True:
				data['location']['latitude'] = data['location']['coordinates'][0]
				data['location']['longitude'] = data['location']['coordinates'][1]
			else:
				data['location']['latitude'] = data['location']['coordinates'][1]
				data['location']['longitude'] = data['location']['coordinates'][0]

		if not (self.order is None):
			try:
				data['order'] = self.order.to_mongo()
				data['order']["id"] = str(self.order.id)
				del data['order']['_id']
			except:
				logging.error('não conseguiu parsear o objeto:'+ str(self.order))
				pass

		if not (self.line is None):
			try:
				data['line'] = self.line.to_mongo()
				data['line']["id"] = str(self.line.id)
				del data['line']['_id']
			except:
				logging.error('não conseguiu parsear o objeto:'+ str(self.line))
				pass
		
		if not (self.route is None):
			try:
				data['route'] = self.route.to_mongo()
				data['route']["id"] = str(self.route.id)
				del data['route']['_id']
			except:
				logging.error('não conseguiu parsear o objeto:'+ str(self.route))
				pass
		
		if not (self.checkin_point is None):
			try:
				data['checkin_point'] = self.checkin_point.to_mongo()
				data['checkin_point']["id"] = str(self.checkin_point.id)
				del data['checkin_point']['_id']

				if self.checkin_point.wrong_location == True:
					data['checkin_point']['location']['latitude'] = data['checkin_point']['location']['coordinates'][0]
					data['checkin_point']['location']['longitude'] = data['checkin_point']['location']['coordinates'][1]
				else:
					data['checkin_point']['location']['latitude'] = data['checkin_point']['location']['coordinates'][1]
					data['checkin_point']['location']['longitude'] = data['checkin_point']['location']['coordinates'][0]
			except:
				logging.error('não conseguiu parsear o objeto:'+ str(self.checkin_point))
				pass

		if not (self.vehicle is None):
			data['vehicle'] = self.vehicle.to_mongo()
			data['vehicle']["id"] = str(self.vehicle.id)
			del data['vehicle']['_id']

			data['vehicle']["gps_updated_at"] = data['vehicle']["gps_updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "gps_updated_at" in data['vehicle'] else None

			if not (self.vehicle.line is None):
				data['vehicle']['line'] = self.vehicle.line.to_mongo()
				data['vehicle']['line']["id"] = str(self.vehicle.line.id)
				del data['vehicle']['line']['_id']

		if not (self.passenger is None):
			data['passenger'] = self.passenger.to_mongo()
			data['passenger']["id"] = str(self.passenger.id)
			del data['passenger']['_id']

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None

		return json_util.dumps(data)

class WorkCalendar(CustomBaseDocument):
	meta = {'collection': 'work_calendar'}

	enterprise 	= ReferenceField('Enterprise')
	name 		= StringField()
	description = StringField()

	def to_json(self, explode_data=False):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

		return json_util.dumps(data)

class WorkSchedule(CustomBaseDocument):
	meta = {'collection': 'work_schedule'}
	
	enterprise 			= ReferenceField('Enterprise')
	work_calendar 		= ReferenceField('WorkCalendar')
	vehicle 			= ReferenceField('Vehicle')
	driver 				= ReferenceField('User')
	line 				= ReferenceField('Line')
	route 				= ReferenceField('Route')
	waypoints 			= EmbeddedDocumentListField(WaypointRoute)
	start_time 			= StringField()
	start_point 		= ReferenceField('Point')
	end_time 			= StringField()
	end_point 			= ReferenceField('Point')
	direction 			= StringField(choices=DIRECTION_OPTIONS)
	is_day_turn_line 	= BooleanField(default=False)
	time_slots			= EmbeddedDocumentListField(TimeSlot)

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None

		if hasattr(self, 'enterprise') and (not (self.enterprise is None)) and (explode_data == True):
			try:
				data['enterprise'] = self.enterprise.to_mongo()
				data['enterprise']["id"] = str(self.enterprise.id)
				del data['enterprise']['_id']
			except:
				pass
		
		if hasattr(self, 'work_calendar') and (not (self.work_calendar is None)) and (explode_data == True):
			try:
				data['work_calendar'] = self.work_calendar.to_mongo()
				data['work_calendar']["id"] = str(self.work_calendar.id)
				del data['work_calendar']['_id']
			except:
				pass

		if hasattr(self, 'vehicle') and (not (self.vehicle is None)) and (explode_data == True):
			try:
				data['vehicle'] = self.vehicle.to_mongo()
				data['vehicle']["id"] = str(self.vehicle.id)
				del data['vehicle']['_id']

				if (self.vehicle.location == False) or (self.vehicle.location is None):
					if 'location' in data['vehicle']:
						del data['vehicle']['location']
				else:
					if self.vehicle.wrong_location == True:
						data['vehicle']['location']['latitude'] = data['vehicle']['location']['coordinates'][0]
						data['vehicle']['location']['longitude'] = data['vehicle']['location']['coordinates'][1]
					else:
						data['vehicle']['location']['latitude'] = data['vehicle']['location']['coordinates'][1]
						data['vehicle']['location']['longitude'] = data['vehicle']['location']['coordinates'][0]
			except:
				pass
		
		if hasattr(self, 'vehicle') and (not (self.driver is None)) and (explode_data == True):
			try:
				data['driver'] = self.driver.to_mongo()
				data['driver']["id"] = str(self.driver.id)
				del data['driver']['_id']
				del data['driver']['password']
			except:
				pass
		
		if (not (self.line is None)) and (explode_data == True):
			data['line'] = self.line.to_mongo()
			data['line']["id"] = str(self.line.id)
			del data['line']['_id']

		if hasattr(self, 'vehicle') and (not (self.route is None)) and (explode_data == True):
			try:
				data['route'] = self.route.to_mongo()
				data['route']["id"] = str(self.route.id)
				del data['route']['_id']

				if not (self.route.subenterprise is None) and (explode_data == True):
					data['route']['subenterprise'] = self.route.subenterprise.to_mongo()
					data['route']['subenterprise']["id"] = str(self.route.subenterprise.id)
					del data['route']['subenterprise']['_id']

				if not (self.route.work_calendars is None) and (explode_data == True):
					data['work_calendars'] = []

					for wc in self.route.work_calendars:
						obj = wc.to_mongo()
						
						obj['work_calendar'] = wc.work_calendar.to_mongo()
						obj['work_calendar']["id"] = str(wc.work_calendar.id)
						del obj['work_calendar']['_id']

						obj['waypoints'] = []
						for wr in wc.waypoints:
							wp = wr.to_mongo()
							
							wp['point'] = wr.point.to_mongo()
							wp['point']["id"] = str(wr.point.id)
							del wp['point']['_id']

							if wr.point.wrong_location == True:
								wp['point']['location']['latitude'] = wp['point']['location']['coordinates'][0]
								wp['point']['location']['longitude'] = wp['point']['location']['coordinates'][1]
							else:
								wp['point']['location']['latitude'] = wp['point']['location']['coordinates'][1]
								wp['point']['location']['longitude'] = wp['point']['location']['coordinates'][0]
							
							wp['point']["created_at"] = wp['point']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in wp['point'] else None
							wp['point']["deleted_at"] = wp['point']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in wp['point'] else None

							obj['waypoints'].append(wp)
						data['work_calendars'].append(obj)	
			except:
				pass
		
		if not (self.waypoints is None) and (explode_data == True):
			data['waypoints'] = []

			for wr in self.waypoints:
				obj = wr.to_mongo()
				
				try:
					obj['point'] = wr.point.to_mongo()
					obj['point']["id"] = str(wr.point.id)
					del obj['point']['_id']

					obj['point']["created_at"] = obj['point']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in obj['point'] else None
					obj['point']["deleted_at"] = obj['point']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in obj['point'] else None

					if wr.point.wrong_location == True:
						obj['point']['location']['latitude'] = obj['point']['location']['coordinates'][0]
						obj['point']['location']['longitude'] = obj['point']['location']['coordinates'][1]
					else:
						obj['point']['location']['latitude'] = obj['point']['location']['coordinates'][1]
						obj['point']['location']['longitude'] = obj['point']['location']['coordinates'][0]
				except:
					del obj['point']

				if not (wr.passengers is None) and len(wr.passengers) > 0:
					obj['passengers'] = []
					
					for passenger in wr.passengers:
						ps = passenger.to_mongo()

						ps['passenger'] = passenger.passenger.to_mongo()
						ps['passenger']["id"] = str(passenger.passenger.id)
						del ps['passenger']['_id']

						ps['passenger']["created_at"] = ps['passenger']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in ps['passenger'] else None
						ps['passenger']["deleted_at"] = ps['passenger']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in ps['passenger'] else None
						
						obj['passengers'].append(ps)

				data['waypoints'].append(obj)
		
		if not (self.time_slots is None) and (explode_data == True):
			data['time_slots'] = []

			for ts in self.time_slots:
				_ts = ts.to_mongo()

				if not(ts.vehicle is None):
					_ts['vehicle'] = ts.vehicle.to_mongo()
					_ts['vehicle']["id"] = str(ts.vehicle.id)
					del _ts['vehicle']['_id']

				if not(ts.driver is None):
					_ts['driver'] = ts.driver.to_mongo()
					_ts['driver']["id"] = str(ts.driver.id)
					del _ts['driver']['_id']
				
				data['time_slots'].append(_ts)
		
		if hasattr(self, 'start_point') and (not (self.start_point is None)) and (explode_data == True):
			try:
				data['start_point'] = self.start_point.to_mongo()
				data['start_point']["id"] = str(self.start_point.id)
				del data['start_point']['_id']

				if self.start_point.wrong_location == True:
					data['start_point']['location']['latitude'] = data['start_point']['location']['coordinates'][0]
					data['start_point']['location']['longitude'] = data['start_point']['location']['coordinates'][1]
				else:
					data['start_point']['location']['latitude'] = data['start_point']['location']['coordinates'][1]
					data['start_point']['location']['longitude'] = data['start_point']['location']['coordinates'][0]
			except:
				pass
		
		if hasattr(self, 'end_point') and (not (self.end_point is None)) and (explode_data == True):
			try:
				data['end_point'] = self.end_point.to_mongo()
				data['end_point']["id"] = str(self.end_point.id)
				del data['end_point']['_id']

				if self.end_point.wrong_location == True:
					data['end_point']['location']['latitude'] = data['end_point']['location']['coordinates'][0]
					data['end_point']['location']['longitude'] = data['end_point']['location']['coordinates'][1]
				else:
					data['end_point']['location']['latitude'] = data['end_point']['location']['coordinates'][1]
					data['end_point']['location']['longitude'] = data['end_point']['location']['coordinates'][0]
			except:
				pass
		
		return json_util.dumps(data)

class Order(CustomBaseDocument):
	meta = {'collection': 'order'}

	enterprise 							= ReferenceField('Enterprise')
	work_schedule 						= ReferenceField('WorkSchedule')
	work_calendar 						= ReferenceField('WorkCalendar')
	vehicle 							= ReferenceField('Vehicle')
	driver 								= ReferenceField('User')
	line 								= ReferenceField('Line')
	route 								= ReferenceField('Route')
	waypoints 							= EmbeddedDocumentListField(WaypointRoute)
	direction 							= StringField(choices=DIRECTION_OPTIONS)
	scheduled_at 						= DateTimeField()
	
	# Order Confirmation Data
	confirmed 							= BooleanField(default=False)
	confirmed_at 						= DateTimeField()
	confirmed_by 						= ReferenceField('User')
	confirm_annotations 				= StringField()

	# Order Accept Data
	accepted 							= BooleanField(default=False)
	accepted_at 						= DateTimeField()
	accept_location 					= PointField()
	
	# Order Departure Place Data (Outcoming Orders)
	arrived_departure_place 			= BooleanField()
	arrived_departure_place_at 			= DateTimeField()
	departure_place_location 			= PointField()

	# Order Start Improdutive Time Data
	start_time 							= StringField()
	start_at 							= DateTimeField()
	start_point 						= ReferenceField('Point')
	started_improdutive_time 			= BooleanField(default=False)
	started_improdutive_time_at 		= DateTimeField()
	started_odometer_value 				= IntField()
	start_location 						= PointField()
	start_vehicle_location 				= PointField()
	
	# Order Start Travel Data
	start_travel_scheduled_at 			= DateTimeField()
	started_travel 						= BooleanField(default=False)
	started_travel_at 					= DateTimeField()
	start_travel_location 				= PointField()
	
	# Order Completed Travel Data
	completed 							= BooleanField(default=False)
	completed_at 						= DateTimeField()
	completed_odometer_value 			= IntField()
	complete_location 					= PointField()
	completed_vehicle_location 			= PointField()
	complete_scheduled_at 				= DateTimeField()
	
	# Order Delivery Data
	end_time 							= StringField()
	end_at 								= DateTimeField()
	end_point 							= ReferenceField('Point')
	delivered 							= BooleanField(default=False)
	delivered_at 						= DateTimeField()
	delivered_odometer_value 			= IntField()
	delivery_location 					= PointField() # TODO: POPULAR CAMPO
	delivered_after_time 				= BooleanField(default=False)
	justification_text 					= StringField()
	finished_automatically 				= BooleanField(default=False)
	
	attachments 						= EmbeddedDocumentListField(Attachment)

	checklist_initial 					= ReferenceField('VehicleCheckListHistory')
	checklist_sanitary 					= ReferenceField('VehicleCheckListHistory')

	customized 							= BooleanField(default=False)
	customized_by 						= ReferenceField('User')

	# Support Vehicle
	support_vehicle 					= ReferenceField('Vehicle')
	support_driver 						= ReferenceField('User')
	support_start_point 				= ReferenceField('Point')
	
	# Order Late Finish
	delivered_after_time_unfounded 		= BooleanField(default=False)
	delivered_after_time_verified 		= BooleanField(default=False)
	delivered_after_time_verified_at 	= DateTimeField()
	delivered_after_time_user_update 	= ReferenceField('User')
	is_valid 							= BooleanField(default=False)
	
	time_slot 							= EmbeddedDocumentField(TimeSlot)
	trips_performed						= EmbeddedDocumentListField(TripPerformed)

	# Order Delay
	is_delayed_vehicle 					= BooleanField(default=False) 
	delayed_at 							= DateTimeField()
	delayed_vehicle_time 				= IntField() # Seconds
	delayed_vehicle_distance			= IntField() # Meters
	chat_room_id						= ObjectIdField()
	
	count_requests = IntField(default=0)
 
	edited_history = ListField()

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']
		
		data["delivered_after_time_verified_at"]= data["delivered_after_time_verified_at"].strftime("%d/%m/%Y %H:%M:%S") if "delivered_after_time_verified_at" in data else None
		data["updated_at"]= data["updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "updated_at" in data else None
		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None
		data["start_at"] = data["start_at"].strftime("%d/%m/%Y %H:%M") if "start_at" in data else None
		data["end_at"] = data["end_at"].strftime("%d/%m/%Y %H:%M") if "end_at" in data else None
		data["scheduled_at"] = data["scheduled_at"].strftime("%d/%m/%Y") if "scheduled_at" in data else None
		data["accepted_at"] = data["accepted_at"].strftime("%d/%m/%Y %H:%M:%S") if "accepted_at" in data else None
		data["confirmed_at"] = data["confirmed_at"].strftime("%d/%m/%Y %H:%M:%S") if "confirmed_at" in data else None
		data["started_improdutive_time_at"] = data["started_improdutive_time_at"].strftime("%d/%m/%Y %H:%M:%S") if "started_improdutive_time_at" in data else None
		data["arrived_departure_place_at"] = data["arrived_departure_place_at"].strftime("%d/%m/%Y %H:%M:%S") if "arrived_departure_place_at" in data else None
		data["start_travel_scheduled_at"] = data["start_travel_scheduled_at"].strftime("%d/%m/%Y %H:%M:%S") if "start_travel_scheduled_at" in data else None
		data["started_travel_at"] = data["started_travel_at"].strftime("%d/%m/%Y %H:%M:%S") if "started_travel_at" in data else None
		data["completed_at"] = data["completed_at"].strftime("%d/%m/%Y %H:%M:%S") if "completed_at" in data else None
		data["complete_scheduled_at"] = data["complete_scheduled_at"].strftime("%d/%m/%Y %H:%M:%S") if "complete_scheduled_at" in data else None
		data["delivered_at"] = data["delivered_at"].strftime("%d/%m/%Y %H:%M:%S") if "delivered_at" in data else None
		data["delayed_at"] = data["delayed_at"].strftime("%d/%m/%Y %H:%M:%S") if "delayed_at" in data else None
		data['chat_room_id'] = self.chat_room_id
		data['count_requests'] = self.count_requests
	
		if self.wrong_location == True:
			if not (self.start_location is None):
				data['start_location']['latitude'] = data['start_location']['coordinates'][0]
				data['start_location']['longitude'] = data['start_location']['coordinates'][1]

			if not (self.completed_vehicle_location is None):
				data['completed_vehicle_location']['latitude'] = data['completed_vehicle_location']['coordinates'][0]
				data['completed_vehicle_location']['longitude'] = data['completed_vehicle_location']['coordinates'][1]
		else:
			if not (self.start_location is None):
				data['start_location']['latitude'] = data['start_location']['coordinates'][1]
				data['start_location']['longitude'] = data['start_location']['coordinates'][0]
			
			if not (self.completed_vehicle_location is None):
				data['completed_vehicle_location']['latitude'] = data['completed_vehicle_location']['coordinates'][1]
				data['completed_vehicle_location']['longitude'] = data['completed_vehicle_location']['coordinates'][0]

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']
		
		try:
			if not (self.work_schedule is None):
				data['work_schedule'] = self.work_schedule.to_mongo()
				data['work_schedule']["id"] = str(self.work_schedule.id)
				del data['work_schedule']['_id']
		except Exception as e:
			logging.error(e)
			pass
		
		if not (self.work_calendar is None):
			data['work_calendar'] = self.work_calendar.to_mongo()
			data['work_calendar']["id"] = str(self.work_calendar.id)
			del data['work_calendar']['_id']
		
		if not (self.vehicle is None):
			data['vehicle'] = self.vehicle.to_mongo()
			data['vehicle']["id"] = str(self.vehicle.id)
			del data['vehicle']['_id']

			data['vehicle']["updated_at"]= data['vehicle']["updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "updated_at" in data['vehicle'] else None
			data['vehicle']["gps_updated_at"]= data['vehicle']["gps_updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "gps_updated_at" in data['vehicle'] else None

			if (self.vehicle.location == False) or (self.vehicle.location is None):
				if 'location' in data['vehicle']:
					del data['vehicle']['location']
			else:
				if self.vehicle.wrong_location == True:
					data['vehicle']['location']['latitude'] = data['vehicle']['location']['coordinates'][0]
					data['vehicle']['location']['longitude'] = data['vehicle']['location']['coordinates'][1]
				else:
					data['vehicle']['location']['latitude'] = data['vehicle']['location']['coordinates'][1]
					data['vehicle']['location']['longitude'] = data['vehicle']['location']['coordinates'][0]
		
		if not (self.support_vehicle is None):
			data['support_vehicle'] = self.support_vehicle.to_mongo()
			data['support_vehicle']["id"] = str(self.support_vehicle.id)
			del data['support_vehicle']['_id']

			data['support_vehicle']["updated_at"]= data['support_vehicle']["updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "updated_at" in data['support_vehicle'] else None
			data['support_vehicle']["gps_updated_at"]= data['support_vehicle']["gps_updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "gps_updated_at" in data['support_vehicle'] else None

			if (self.support_vehicle.location == False) or (self.support_vehicle.location is None):
				if 'location' in data['support_vehicle']:
					del data['support_vehicle']['location']
			else:
				if self.support_vehicle.wrong_location == True:
					data['support_vehicle']['location']['latitude'] = data['support_vehicle']['location']['coordinates'][0]
					data['support_vehicle']['location']['longitude'] = data['support_vehicle']['location']['coordinates'][1]
				else:
					data['support_vehicle']['location']['latitude'] = data['support_vehicle']['location']['coordinates'][1]
					data['support_vehicle']['location']['longitude'] = data['support_vehicle']['location']['coordinates'][0]

		if not (self.line is None):
			data['line'] = self.line.to_mongo()
			data['line']["id"] = str(self.line.id)
			del data['line']['_id']

		if not (self.route is None):
			data['route'] = self.route.to_mongo()
			data['route']["id"] = str(self.route.id)
			del data['route']['_id']

			if not (self.route.subenterprise is None):
				data['route']['subenterprise'] = self.route.subenterprise.to_mongo()
				data['route']['subenterprise']["id"] = str(self.route.subenterprise.id)
				del data['route']['subenterprise']['_id']
			
			data['route']['work_calendars'] = []

			for wc in self.route.work_calendars:
				obj = wc.to_mongo()
				
				obj['work_calendar'] = wc.work_calendar.to_mongo()
				obj['work_calendar']["id"] = str(wc.work_calendar.id)
				del obj['work_calendar']['_id']

				data['route']['work_calendars'].append(obj)
			
		if not (self.waypoints is None):
			data['waypoints'] = []

			for wr in self.waypoints:
				obj = wr.to_mongo()
				
				obj['point'] = wr.point.to_mongo()
				obj['point']["id"] = str(wr.point.id)
				del obj['point']['_id']

				obj['point']["created_at"] = obj['point']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in obj['point'] else None
				obj['point']["deleted_at"] = obj['point']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in obj['point'] else None

				if wr.point.wrong_location == True:
					obj['point']['location']['latitude'] = obj['point']['location']['coordinates'][0]
					obj['point']['location']['longitude'] = obj['point']['location']['coordinates'][1]
				else:
					obj['point']['location']['latitude'] = obj['point']['location']['coordinates'][1]
					obj['point']['location']['longitude'] = obj['point']['location']['coordinates'][0]

				obj["executed_at"] = obj["executed_at"].strftime("%d/%m/%Y %H:%M:%S") if "executed_at" in obj else None
				obj["scheduled_at"] = obj["scheduled_at"].strftime("%d/%m/%Y %H:%M:%S") if "scheduled_at" in obj else None

				if not (wr.passengers is None) and len(wr.passengers) > 0:
					obj['passengers'] = []
					
					for passenger in wr.passengers:
						ps = passenger.to_mongo()

						ps["updated_at"] = ps["updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "updated_at" in ps else None

						ps['passenger'] = passenger.passenger.to_mongo()
						ps['passenger']["id"] = str(passenger.passenger.id)
						del ps['passenger']['_id']

						ps['passenger']["created_at"] = ps['passenger']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in ps['passenger'] else None
						ps['passenger']["deleted_at"] = ps['passenger']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in ps['passenger'] else None
						
						obj['passengers'].append(ps)

				if wr.status is None:
					obj['status'] = 'pending'

				data['waypoints'].append(obj)
		
		if not (self.start_point is None):
			data['start_point'] = self.start_point.to_mongo()
			data['start_point']["id"] = str(self.start_point.id)
			del data['start_point']['_id']

			if self.start_point.wrong_location == True:
				data['start_point']['location']['latitude'] = data['start_point']['location']['coordinates'][0]
				data['start_point']['location']['longitude'] = data['start_point']['location']['coordinates'][1]
			else:
				data['start_point']['location']['latitude'] = data['start_point']['location']['coordinates'][1]
				data['start_point']['location']['longitude'] = data['start_point']['location']['coordinates'][0]
		
		if not (self.end_point is None):
			data['end_point'] = self.end_point.to_mongo()
			data['end_point']["id"] = str(self.end_point.id)
			del data['end_point']['_id']

			if self.end_point.wrong_location == True:
				data['end_point']['location']['latitude'] = data['end_point']['location']['coordinates'][0]
				data['end_point']['location']['longitude'] = data['end_point']['location']['coordinates'][1]
			else:
				data['end_point']['location']['latitude'] = data['end_point']['location']['coordinates'][1]
				data['end_point']['location']['longitude'] = data['end_point']['location']['coordinates'][0]
		
		if not (self.delivered_after_time_user_update is None):
			data['delivered_after_time_user_update'] = self.delivered_after_time_user_update.to_mongo()
			data['delivered_after_time_user_update']["id"] = str(self.delivered_after_time_user_update.id)
			del data['delivered_after_time_user_update']['_id']
			
		if not (self.driver is None):
			data['driver'] = self.driver.to_mongo()
			data['driver']["id"] = str(self.driver.id)
			del data['driver']['_id']
		
		if not (self.support_driver is None):
			data['support_driver'] = self.support_driver.to_mongo()
			data['support_driver']["id"] = str(self.support_driver.id)
			del data['support_driver']['_id']
		
		try:
			if not (self.confirmed_by is None):
				data['confirmed_by'] = self.confirmed_by.to_mongo()
				data['confirmed_by']["id"] = str(self.confirmed_by.id)
				del data['confirmed_by']['_id']
		except Exception as e:
			logging.error(e)
			pass
		
		if not (self.checklist_initial is None):
			data['checklist_initial'] = self.checklist_initial.to_mongo()
			data['checklist_initial']["id"] = str(self.checklist_initial.id)
			del data['checklist_initial']['_id']

			data['checklist_initial']["created_at"] = data['checklist_initial']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['checklist_initial'] else None
		
		if not (self.checklist_sanitary is None):
			data['checklist_sanitary'] = self.checklist_sanitary.to_mongo()
			data['checklist_sanitary']["id"] = str(self.checklist_sanitary.id)
			del data['checklist_sanitary']['_id']

			data['checklist_sanitary']["created_at"] = data['checklist_sanitary']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['checklist_sanitary'] else None
		
		if not (self.customized_by is None):
			data['customized_by'] = self.customized_by.to_mongo()
			data['customized_by']["id"] = str(self.customized_by.id)
			del data['customized_by']['_id']

		if not(self.time_slot is None):
			data['time_slot'] = self.time_slot.to_mongo()
			if not(self.time_slot.vehicle is None):
				data['time_slot']['vehicle'] = self.time_slot.vehicle.to_mongo()
				data['time_slot']['vehicle']["id"] = str(self.time_slot.vehicle.id)
				del data['time_slot']['vehicle']['_id']

			if not(self.time_slot.driver is None):
				data['time_slot']['driver'] = self.time_slot.driver.to_mongo()
				data['time_slot']['driver']["id"] = str(self.time_slot.driver.id)
				del data['time_slot']['driver']['_id']

		if not (self.trips_performed is None):
			data['trips_performed'] = []

			for tp in self.trips_performed:
				obj = tp.to_mongo()
				
				obj["executed_at"] = obj["executed_at"].strftime("%d/%m/%Y %H:%M:%S") if "executed_at" in obj else None

				obj['boarding_point'] = tp.boarding_point.to_mongo()
				obj['boarding_point']['id'] = str(tp.boarding_point.id)
				del obj['boarding_point']['_id']
				
				if not (tp.passengers_boarded is None) and len(tp.passengers_boarded) > 0:
					obj['passengers_boarded'] = []

					for ps in tp.passengers_boarded:
						_ps = ps.to_mongo()

						_ps["updated_at"] = _ps["updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "updated_at" in _ps else None

						_ps = passenger.passenger.to_mongo()
						_ps["id"] = str(passenger.passenger.id)
						del _ps['_id']

						_ps["created_at"] = _ps["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in _ps else None
						_ps["deleted_at"] = _ps["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in _ps else None
						
						obj['passengers_boarded'].append(_ps)
				
				data['trips_performed'].append(obj)		
		return json_util.dumps(data)

class RepairCategory(CustomBaseDocument):
	meta = {'collection': 'repair_categories'}

	description = StringField()
	enterprise 	= ReferenceField('Enterprise')
	parent = ReferenceField('RepairCategory')

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']
		
		if not (self.parent is None):
			data['parent'] = self.parent.to_mongo()
			data['parent']["id"] = str(self.parent.id)
			del data['parent']['_id']

		return json_util.dumps(data)

class RepairRequest(CustomBaseDocument):
	meta = {'collection': 'repair_requests'}

	enterprise = ReferenceField('Enterprise')
	requester = ReferenceField('User')
	vehicle = ReferenceField('Vehicle')
	title = StringField()
	category = ReferenceField('RepairCategory')
	additional_info = StringField()
	engineer = ReferenceField('User')
	engineer_comments = StringField()
	status = StringField(choices=REPAIR_REQUEST_STATUS, default="pending")
	priority = StringField(choices=REPAIR_REQUEST_PRIORITY, default="low")
	location = PointField()
	attachments = EmbeddedDocumentListField(Attachment)

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']
		
		if not (self.requester is None):
			data['requester'] = self.requester.to_mongo()
			data['requester']["id"] = str(self.requester.id)
			del data['requester']['_id']
		
		if not (self.category is None):
			data['category'] = self.category.to_mongo()
			data['category']["id"] = str(self.category.id)
			del data['category']['_id']
		
		if not (self.vehicle is None):
			data['vehicle'] = self.vehicle.to_mongo()
			data['vehicle']["id"] = str(self.vehicle.id)
			del data['vehicle']['_id']

		if not (self.engineer is None):
			data['engineer'] = self.engineer.to_mongo()
			data['engineer']["id"] = str(self.engineer.id)
			del data['engineer']['_id']
		
		if not(self.location == False) and not(self.location is None):
			if self.wrong_location == True:
				data['location']['latitude'] = data['location']['coordinates'][0]
				data['location']['longitude'] = data['location']['coordinates'][1]
			else:
				data['location']['latitude'] = data['location']['coordinates'][1]
				data['location']['longitude'] = data['location']['coordinates'][0]

		return json_util.dumps(data)

class FuelSupplyRecord(CustomBaseDocument):
	meta = {'collection': 'fuel_supply_records'}

	enterprise = ReferenceField('Enterprise')
	user = ReferenceField('User')
	vehicle = ReferenceField('Vehicle')
	origin = StringField()
	odometer_value = FloatField()
	supply_value = FloatField()
	total_amount = FloatField()
	attachments = EmbeddedDocumentListField(Attachment)
	location = PointField()
	verified = BooleanField(default=False)
	note = StringField()

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']
		
		if not (self.user is None):
			data['user'] = self.user.to_mongo()
			data['user']["id"] = str(self.user.id)
			del data['user']['_id']
		
		if not (self.vehicle is None):
			data['vehicle'] = self.vehicle.to_mongo()
			data['vehicle']["id"] = str(self.vehicle.id)
			del data['vehicle']['_id']
		
		if not(self.location == False) and not(self.location is None):
			if self.wrong_location == True:
				data['location']['latitude'] = data['location']['coordinates'][0]
				data['location']['longitude'] = data['location']['coordinates'][1]
			else:
				data['location']['latitude'] = data['location']['coordinates'][1]
				data['location']['longitude'] = data['location']['coordinates'][0]

		return json_util.dumps(data)

class Event(CustomBaseDocument):
	meta = {'collection': 'events'}

	enterprise = ReferenceField('Enterprise')
	vehicle = ReferenceField('Vehicle')
	gps_update_font = StringField(default='vehicle-tracker', choices=GPS_UPDATE_FONTS)
	driver = ReferenceField('User')
	order = ReferenceField('Order')
	event_type = StringField(choices=EVENT_TYPES)
	event_data = EmbeddedDocumentListField(EventDataRecord)
	location = PointField()
	address = EmbeddedDocumentField(AddressInfo)
	location_time = DateTimeField()
	verified = BooleanField(default=False)
	is_valid = BooleanField(default=False)

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["updated_at"] = data["updated_at"].strftime("%d/%m/%Y %H:%M:%S") if "updated_at" in data else None
		data["deleted_at"] = data["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data else None
		data["location_time"] = data["location_time"].strftime("%d/%m/%Y %H:%M:%S") if "location_time" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']
		
		if not (self.vehicle is None):
			data['vehicle'] = self.vehicle.to_mongo()
			data['vehicle']["id"] = str(self.vehicle.id)
			del data['vehicle']['_id']
		
		if not (self.driver is None):
			data['driver'] = self.driver.to_mongo()
			data['driver']["id"] = str(self.driver.id)
			del data['driver']['_id']
		
		if not (self.user_update is None):
			data['user_update'] = self.user_update.to_mongo()
			data['user_update']["id"] = str(self.user_update.id)
			del data['user_update']['_id']
		
		if not (self.order is None):
			data['order'] = self.order.to_mongo()
			data['order']["id"] = str(self.order.id)
			del data['order']['_id']

			data['order']['route'] = self.order.route.to_mongo()
			data['order']['route']["id"] = str(self.order.route.id)
			del data['order']['route']['_id']
		
		if not(self.location == False) and not(self.location is None):
			if self.wrong_location == True:
				data['location']['latitude'] = data['location']['coordinates'][0]
				data['location']['longitude'] = data['location']['coordinates'][1]
			else:
				data['location']['latitude'] = data['location']['coordinates'][1]
				data['location']['longitude'] = data['location']['coordinates'][0]

		return json_util.dumps(data)

class VehicleCostItem(CustomBaseDocument):
	meta = {'collection': 'vehicle_cost_items'}

	name = StringField()
	formula = StringField()
	description = StringField()
	enterprise = ReferenceField('Enterprise')

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None

		return json_util.dumps(data)

class VehicleType(CustomBaseDocument):
	meta = {'collection': 'vehicle_types'}

	name = StringField()
	icon = StringField()
	cost_items = EmbeddedDocumentListField(VehicleTypeCostItem)
	enterprise = ReferenceField('Enterprise')

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None

		if not (self.cost_items is None):
			data['cost_items'] = []

			for cost_items in self.cost_items:
				obj = cost_items.to_mongo()

				if not (cost_items.cost_item is None):
					obj['cost_item'] = cost_items.cost_item.to_mongo()
					obj['cost_item']["id"] = str(cost_items.cost_item.id)
					del obj['cost_item']['_id']

				data['cost_items'].append(obj)

		return json_util.dumps(data)

class ServiceRating(CustomBaseDocument):
	meta = {'collection': 'service_ratings'}

	enterprise 		= ReferenceField('Enterprise')
	subenterprise 	= ReferenceField('SubEnterprise')
	passenger 		= ReferenceField('Passenger')
	vehicle 		= ReferenceField('Vehicle')
	items 			= EmbeddedDocumentListField(RatingItem)

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None

		if not (self.subenterprise is None):
			data['subenterprise'] = self.subenterprise.to_mongo()
			data['subenterprise']["id"] = str(self.subenterprise.id)
			del data['subenterprise']['_id']

			data['subenterprise']["created_at"] = data['subenterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['subenterprise'] else None
			data['subenterprise']["deleted_at"] = data['subenterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['subenterprise'] else None
		
		if not (self.passenger is None):
			data['passenger'] = self.passenger.to_mongo()
			data['passenger']["id"] = str(self.passenger.id)
			del data['passenger']['_id']

			data['passenger']["created_at"] = data['passenger']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['passenger'] else None
			data['passenger']["deleted_at"] = data['passenger']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['passenger'] else None
		
		if not (self.vehicle is None):
			data['vehicle'] = self.vehicle.to_mongo()
			data['vehicle']["id"] = str(self.vehicle.id)
			del data['vehicle']['_id']

			data['vehicle']["created_at"] = data['vehicle']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['vehicle'] else None
			data['vehicle']["deleted_at"] = data['vehicle']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['vehicle'] else None

		return json_util.dumps(data)

class TachographRecord(CustomBaseDocument):
	meta = {'collection': 'tachograph_record'}

	enterprise 	 = ReferenceField('Enterprise')
	driver 		 = ReferenceField('User')
	vehicle 	 = ReferenceField('Vehicle')
	attachment 	 = EmbeddedDocumentField(Attachment)
	scheduled_at = DateTimeField()

	def to_json(self, explode_data=True):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		data["created_at"] = data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None
		data["scheduled_at"] = data["scheduled_at"].strftime("%d/%m/%Y") if "scheduled_at" in data else None

		if not (self.enterprise is None):
			data['enterprise'] = self.enterprise.to_mongo()
			data['enterprise']["id"] = str(self.enterprise.id)
			del data['enterprise']['_id']

			data['enterprise']["created_at"] = data['enterprise']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['enterprise'] else None
			data['enterprise']["deleted_at"] = data['enterprise']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['enterprise'] else None

		if not (self.driver is None):
			data['driver'] = self.driver.to_mongo()
			data['driver']["id"] = str(self.driver.id)
			del data['driver']['_id']
			del data['driver']['password']

			data['driver']["created_at"] = data['driver']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['driver'] else None
			data['driver']["deleted_at"] = data['driver']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['driver'] else None
		
		if not (self.vehicle is None):
			data['vehicle'] = self.vehicle.to_mongo()
			data['vehicle']["id"] = str(self.vehicle.id)
			del data['vehicle']['_id']

			data['vehicle']["created_at"] = data['vehicle']["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data['vehicle'] else None
			data['vehicle']["deleted_at"] = data['vehicle']["deleted_at"].strftime("%d/%m/%Y %H:%M:%S") if "deleted_at" in data['vehicle'] else None

		return json_util.dumps(data)
	
class VehicleTrakerHistory(CustomBaseDocument):
	meta = {'collection': 'vehicle_traker_histories'}

	enterprise 	 	= ReferenceField('Enterprise')
	order			= ReferenceField('Order')
	path			= MultiPointField()

	def to_json(self, explode_data=True):
		data = self.to_mongo()

		del data['enterprise']
		del data['_id']

		data["id"] 				= str(self.id)
		data["enterprise_id"]	= str(self.enterprise.id)
		data["path"] 			= self.path
		data["created_at"] 		= data["created_at"].strftime("%d/%m/%Y %H:%M:%S") if "created_at" in data else None

		if not (self.order is None):
			data['order'] = self.order.to_mongo()
			data['order']["id"] = str(self.order.id)
			del data['order']['_id']

			data['order']['route']		= self.order.route.to_mongo()
			data['order']['vehicle'] 	= self.order.vehicle.to_mongo()
			data['order']['driver'] 	= self.order.driver.to_mongo()


		return json_util.dumps(data, default=None)

class MileageReport(Document):
	meta = {'collection': 'mileage_reports'}

	enterprise  						= ReferenceField('Enterprise')
	subenterprise						= ObjectIdField()
	order                            	= ReferenceField('Order')
	driver                              = ReferenceField('User')
	vehicle                             = ReferenceField('Vehicle')
	route                               = ReferenceField('Route')
	started_improdutive_time_at        	= DateTimeField()
	started_travel_at                   = DateTimeField()
	completed_at                        = DateTimeField()
	delivered_at                        = DateTimeField()
	fulfilled_km_improdutive_init    	= FloatField()
	fulfilled_km_improdutive_end       	= FloatField()
	fulfilled_km_productive            	= FloatField()
	provided_km_improdutive_init		= FloatField()
	provided_km_improdutive_end			= FloatField()
	provided_km_productive				= FloatField()
	working_hours                       = StringField()
	information                         = StringField()
	direction                           = StringField()
	scheduled_at 						= DateTimeField()
	created_at 							= DateTimeField(default=datetime.datetime.now)
	updated_at 							= DateTimeField()
 
 
class Notification(Document):
	meta = {'collection': 'notifications'}

	TYPE_CHOICES = (('mileage_report', 'mileage_report'))
 
	user 		= ReferenceField(User, required=True)
	order 		= ReferenceField(Order, required=True)
	type 		= StringField(choices=TYPE_CHOICES, required=True)
	title 		= StringField(required=True)
	body 		= StringField(required=True)
	read 		= BooleanField(default=False)
	created_at	= DateTimeField(default=datetime.datetime.now)