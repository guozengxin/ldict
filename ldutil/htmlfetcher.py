#!/usr/bin/env python
#encoding=utf-8

import urllib2
from urllib2 import HTTPError, URLError
from StringIO import StringIO
import sys
from gzipSupport import ContentEncodingProcessor

def get_headers():
	header = {
			'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22'
			}
	return header

def http_get_response(url, referer = None):
	'''get html response from web'''
	response = None
	encoding_support = ContentEncodingProcessor
	opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
	try:
		headers = get_headers()
		if referer is not None:
			headers['Referer'] = referer
		request = urllib2.Request(url, headers = headers)
		response = opener.open(request, timeout=20)
	except HTTPError, e:
		sys.stderr.write(str(e) + '\n')
	except URLError, e:
		sys.stderr.write(str(e) + '\n')
	except IOError, e:
		sys.stderr.write(str(e) + '\n')
#	except:
#		sys.stderr.write('unknown error in http_get_response\n')
	return response

def http_get(url, referer = None):
	'''get html file from web'''
	data = None
	response = http_get_response(url, referer)
	if response:
		try:
			data = response.read()
		except:
			sys.stderr.write('unnkown error in http_get')
	return data

