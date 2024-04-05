from src.utils import ConfigPropertiesHelper


class GetrakMiddleware(object):

	def __init__(self):
		self.api_url = 'https://api.getrak-middleware.8x-esystem.com.br'
		self.cph = ConfigPropertiesHelper()
		MONGODB_ENVIRONMENT = self.cph.get_property_value('GETRAK-MIDDLEWARE-API', 'getrak.middleware.api.environment')
		self.token = self.cph.get_property_value('GETRAK-MIDDLEWARE-API', f'getrak.middleware.api.{MONGODB_ENVIRONMENT}.token')
		self.client_id = self.cph.get_property_value('GETRAK-MIDDLEWARE-API', 'getrak_middleware.client_id')

	def make_url(self, paths):
		url = self.api_url
		for path in paths:
			url = url +'/'+ str(path)
		return url