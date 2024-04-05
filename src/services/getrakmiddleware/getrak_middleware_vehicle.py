import sys
import requests

from src.services.getrakmiddleware.getrak_middleware import GetrakMiddleware
from src.utils import ConfigPropertiesHelper

class GetrakMiddlewareVehicle(GetrakMiddleware):
    
	def get_all(self):
		try:
			url = self.make_url(['vehicles'])
			headers = {
				'x-api-token': self.token,
			}
			res = requests.get(url, headers=headers)
			res.raise_for_status()
			data = res.json()
			return data
		except Exception as e:
			print(f'Error ocurred: {str(e)} on {sys.exc_info()[-1].tb_lineno}')
			return {
				'status': 'error',
				'message': f'Error ocurred: {str(e)} on {sys.exc_info()[-1].tb_lineno}'
			}

	def get_by_id(self, id):
		try:
			url = self.make_url(['vehicle', id])
			headers = {
				'x-api-token': self.token,
			}

			res = requests.get(url, headers=headers)
			res.raise_for_status()
			data = res.json()
			return data
		except Exception as e:
			print(f'Error ocurred: {str(e)} on {sys.exc_info()[-1].tb_lineno}')
			return {
				'status': 'error',
				'message': f'Error ocurred: {str(e)} on {sys.exc_info()[-1].tb_lineno}'
			}