#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import requests
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("api.conf")
username = config.get('zoomeye', 'username')
password = config.get('zoomeye', 'password')

def zoomeye_search(word):

	try:

		data = '{ "username": "'+username+'", "password": "'+password+'" }'
		response = requests.post('https://api.zoomeye.org/user/login', data=data)
		token = response.json()['access_token']

	except:

		print("[-] We got an error with your zoomeye credentials. (Check if zoomeye is down ¯\_(ツ)_/¯)")
		exit(1)


	try:

		headers = {
		    'Authorization': 'JWT {0}'.format(token),
		}

		params = {
		    ('query', 'title: "{0}"'.format(word))
		}

		response = requests.get('https://api.zoomeye.org/host/search', headers=headers, params=params)
		final = response.json()['matches']
		title_result = set([host['ip'] for host in final])
		if title_result:
			return title_result

	except:

		print("[-] We got an error here!")
		exit(1)
		