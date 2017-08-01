#!/usr/bin/python
import socket, os, time, re
import urllib2
from aws.route53_dyndns import settings
# from settings import Settings
from area53 import route53
from boto.route53 import connection, record
import boto3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(settings.log_level)

def get_connection():
	global cfg, logger
	#establish a connection to route53
	if settings.log_level is logging.DEBUG:
		aws_log_level = 2
	else:
		aws_log_level = 0	
	logger.debug('Access key is %s###' % cfg.access_key)
	aws = boto3.session.Session(aws_access_key_id=cfg.access_key,
					aws_secret_access_key=cfg.secret_key)
	logger.debug('Access key is %s###' % cfg.access_key)
	print aws.get_available_resources()
	# boto3.session.client('route
			     # aws_access_key_id=cfg.access_key,
			     # aws_secret_access_key=cfg.secret_key)
	# aws = connection.Route53Connection(cfg.access_key,
					   # cfg.secret_key,
					   # debug=aws_log_level,
					   # security_token=None)
	return aws


def get_external_ip():
	ip_search = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
	data = urllib2.urlopen('http://www.ipaddress.com').read()
	ip = ip_search.findall(data)
	if ip:
		logger.info('found current ip to be:%s' % ip[0])
		ip = ip[0]
	else:
		logger.error('could not find external ip')
	return ip


def find_zone(zones, zone_name):
	for zone in zones:
		logger.debug('checking zone with ID %s and name %s\n \
			matching zone with name %s' % (zone.id, zone.name, zone_name))
		if zone.name == zone_name:
			logger.debug('found zone with ID %s and name %s' % (zone.id, zone.name))
			return zone	


def define_update_record(zone_name, record_name, new_ip):
	global cfg
	aws = get_connection()
	# zones = aws.get_zones()
	# logger.debug('Getting zone with name %s' % zone_name)
	# zone = aws.get_zone(zone_name)
	# zone = find_zone(zones, zone_name)
	# logger.debug('Found zone matching name %s with id %s' % (zone.name, zone.id))
	# logger.debug('modifying record with name %s' % record_name)
	# # Retreiving current IP address of record
	# current_rrsets = aws.get_all_rrsets(zone.id)
	# current_ip = None
	# for rrset in current_rrsets:
		# if record_name in rrset.to_xml():
			# current_ip = rrset.to_xml().split('<Value>')[1].split('</Value>')[0]
			# logger.debug("Current IP address is: %s" % current_ip)
	# updates = record.ResourceRecordSets(aws, zone.id)
	# # Delete current record with old IP
	# rrecord = updates.add_change('DELETE', 
				# record_name,
				# 'A',
				# 300
				# )
	# rrecord.add_value(current_ip)
	# rrecord = updates.add_change('CREATE', 
				# record_name,
				# 'A',
				# 300
				# )
	# rrecord.add_value(new_ip)
	# updates.commit()



# use area53 to update a record give name and ip and strings
def area53_update_record(zone_name, name, ip):
	zone = route53.get_zone(zone_name)
	for record in zone.get_records():
		print(record)


if __name__ == '__main__':
	cfg = settings.Settings()
	# Get info for updating AWS
	ip = get_external_ip()
	zone = cfg.zone_name
	record_name = cfg.record_name
	define_update_record(zone, record_name, ip)

