from boto.route53 import connection
from boto.pyami import config
import boto
import ConfigParser

from area53 import route53
import logging

#Setup logging
log_level = logging.DEBUG
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(log_level)


class Settings(object):

	config = None
	access_key = None
	secret_key = None
	zone_name = 'scdangit.com'
	record_name = 'pollenoffice.scdangit.com'

	def __init__(self):
		self.get_config()
	
	# Load Configuration paraneters
	def get_config(self):
		self.config =ConfigParser.ConfigParser()
		self.config.read('/etc/boto.cfg')
		self.access_key = self.config.get('Credentials', 'aws_access_key_id')
		self.secret_key = self.config.get('Credentials', 'aws_secret_access_key')

# use area53 to update a record give name and ip and strings
def area53_update_record(zone_name, name, ip):
	zone = route53.get_zone(zone_name)
	for record in zone.get_records():
		print(record)


if __name__ == '__main__':
	#establish a connection to route53
	cfg = Settings()
	logger.debug('Access key is %s###' % cfg.access_key)
	logger.debug('Secret key is %s###' % cfg.secret_key)
	aws = connection.Route53Connection(cfg.access_key,
					   cfg.secret_key,
					   debug=2)

#aws_access_key_id=cfg.access_key,
					   #aws_secret_access_key=cfg.secret_key)
	#aws = boto.connect_route53(cfg.access_key,
				   #cfg.secret_key)
	logger.debug('got connection sith host %s and api version %s' % (aws.DefaultHost, aws.Version))
	index, zones = aws.get_zones()
	logger.debug('zone index:%d number of zones:%d' % (index, len(zones)))
					   
