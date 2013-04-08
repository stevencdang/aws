import socket, os, time, re
import urllib2
import settings
from settings import Settings
from area53 import route53
import logging

logger = logging.getLogger(__name__)
logger.setLevel(settings.log_level)
cfg = settings.Settings()

def get_connection():
	global cfg, logger
	#establish a connection to route53
	if settings.log_level is logging.DEBUG:
		aws_log_level = 2
	else:
		aws_log_level = 0	
	logger.debug('Access key is %s###' % cfg.access_key)
	aws = connection.Route53Connection(cfg.access_key,
					   cfg.secret_key,
					   debug=aws_log_level,
					   security_token=None)
	return aws


def get_external_ip():
	ip_search = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
	data = urllib2.urlopen('http://www.ipchicken.com').read()
	ip = ip_search.findall(data)
	if ip:
		logger.info('found current ip to be:%s' % ip[0])
		ip = ip[0]
	else:
		logger.error('could not find external ip')
	return ip


def find_zone(zones, zone_name):
	for zone in zones:
		if zone['Name'] is zone_name:
			return zone	


def define_update_record(zone_name, record_name, ip):
	global cfg
	aws = get_connections()
	zones = aws.get_zones()
	zone = find_zone(zones, zone_name)
	zone_id = zone['ID'].replace('/hostedzone/','')
	logger.debug('Found zone matching name %s with id %s' % (zone_name, zone_id))
	#updates = ResourceRecordsSets(aws, cfg.zone_id)
	#update = updates.add_change(


# use area53 to update a record give name and ip and strings
def area53_update_record(zone_name, name, ip):
	zone = route53.get_zone(zone_name)
	for record in zone.get_records():
		print(record)


if __name__ == '__main__':
	cfg = Settings()
	# Get info for updating AWS
	ip = get_external_ip()
	zone = cfg.zone_name
	record = cfg.record_name
	define_(zone, record, ip)

	
