#!/usr/bin/python
import socket, os, time, re
import copy
import urllib2
from aws.route53_dyndns import settings
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
	logger.debug('Access key is %s' % cfg.access_key)
	
	aws = boto3.client('route53')
	# aws = connection.Route53Connection(cfg.access_key,
	# 				   cfg.secret_key,
	# 				   debug=aws_log_level,
	# 				   security_token=None)
	return aws


def get_external_ip():
        # Get the ip address using a specific site
        data = urllib2.urlopen("http://checkip.dyndns.org/").read()
        # Search the result page for an ip address
	ip_search = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
	ip = ip_search.findall(data)
        # Return the result or log the error
	if ip:
		logger.info('found current ip to be:%s' % ip[0])
		ip = ip[0]
	else:
		logger.error('could not find external ip')
	return ip


def find_zone(zones, zone_name):
    logger.debug(zones)
    for zone in zones:
	logger.debug(zone)
        logger.debug('checking zone with ID %s and name %s\n \
                matching zone with name %s' % (zone['Id'], zone['Name'], zone_name))
        if zone['Name'] == zone_name:
                logger.debug('found zone with ID %s and name %s' % (zone['Id'], zone['Name']))
                return zone	
        else:
            logger.debug("Ignoring zone with name: %s" % zone)


def define_update_record(zone_name, record_name, new_ip):
	global cfg
        # Connect to AWS
	aws = get_connection()
        # Get list of hosted zones and select the target to update base on parameters
	response = aws.list_hosted_zones()
	zones = response['HostedZones']
	logger.debug('Getting zone with name %s' % zone_name)
	zone = find_zone(zones, zone_name)
	logger.debug('Found zone matching name %s with id %s' % (zone['Name'], zone['Id']))
	logger.debug('modifying record with name %s' % record_name)
	# Retreiving current IP address of record
	response = aws.list_resource_record_sets(
		HostedZoneId=zone['Id'])
	current_rrsets = response['ResourceRecordSets']
	# logger.debug(current_rrsets)
	current_ip = None
	cur_rrset = None
	for rrset in current_rrsets:
            if record_name in rrset['Name']:
		cur_rrset = rrset
		current_ip = rrset['ResourceRecords'][0]['Value']
                logger.info("Current IP address is: %s" % current_ip)
	if current_ip != new_ip:
		new_rrset = copy.deepcopy(cur_rrset)
		new_rrset['ResourceRecords'][0]['Value'] = new_ip
		change_request = {
			'Comment': "Changing IP from %s to %s" % (current_ip, new_ip),
			'Changes': [
				{
					'Action': 'DELETE',
					'ResourceRecordSet': cur_rrset
				},
				{
					'Action': 'CREATE',
					'ResourceRecordSet': new_rrset
				},
			]

		}
		logger.debug("Submitting change request for hosted zone %s: %s" % (zone['Id'], str(change_request)))

		response = aws.change_resource_record_sets(
			HostedZoneId=zone['Id'],
			ChangeBatch=change_request
		)
		logger.debug("Got record change response: %s" % str(response))
		logger.info("Completed update to new ip: %s" % new_ip)
	else:
		logger.info("No need to update, ip is the same as previous")


if __name__ == '__main__':
	cfg = settings.Settings()
	# Get info for updating AWS
	ip = get_external_ip()
	zone = cfg.zone_name
	record_name = cfg.record_name

	define_update_record(zone, record_name, ip)

