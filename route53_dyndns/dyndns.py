import socket, os
import urllib2
import settings
import logging

logger = logging.getLogger(__name__)
logger.setLevel(settings.log_level)


def get_external_ip():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(('google.com', 80))
	ip = sock.getsockname()[0]
	sock.close()
	logger.info('current extenal ip is %s' % ip)
	return ip


def get_external_ip2():
	fqn = os.uname()[1]
	ip = urllib2.urlopen('http://whatismyip.org').read()
	logger.info('current extenal ip is %s' % ip)
	return ip


if __name__ == '__main__':
	ip = get_external_ip()
	ip = get_external_ip2()
	
