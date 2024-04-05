import sys
import requests
from services.getrakmiddleware.getrak_middleware import GetrakMiddleware
from src.utils import ConfigPropertiesHelper

class GetrakMiddlewareTrackerHistory(GetrakMiddleware):
    
	def get_tracker_history(self, vehicle_id, dta_from, dta_to):
		try:
			url = self.make_url(['vehicle', vehicle_id, 'tracker-history'])
   
			headers = {
				'x-api-token': self.token,
			}

			params = {}
			if dta_from:
					params['dta_from'] = dta_from
			if dta_to:
					params['dta_to'] = dta_to
			
			res = requests.get(url, params=params, headers=headers)
			res.raise_for_status()
			data = res.json()
			return data
		except Exception as e:
			return {
				'status': 'error',
				'message': f'Error ocurred: {str(e)} on {sys.exc_info()[-1].tb_lineno}'
			}