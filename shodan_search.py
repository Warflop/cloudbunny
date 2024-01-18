#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from prettytable import PrettyTable
from shodan import Shodan
import configparser
import requests

config = configparser.ConfigParser()
config.read("api.conf")
token = config.get('shodan', 'token')
api = Shodan(token)

def test_api_shodan(token):

	response = requests.get("https://api.shodan.io/api-info?key={0}".format(token))
	if response.status_code != 200:
		print("[-] We got an error with your shodan credentials.")
		exit(1)		

def shodan_search(word):

	test_api_shodan(token)

	try:

		banner = api.search_cursor('http.title:"{0}"'.format(word))
		title_result = set([host['ip_str'] for host in banner])
		if title_result:
			return title_result

	except:

		print("[-] We got an error here!")
		exit(1)

def result_search(list_host):

	table = PrettyTable(['IP Address','ISP','Ports','Last Update'])

	for check in list_host:
		try:
			host_result = api.host(check)
			table.add_row([host_result['ip_str'], host_result['isp'], host_result['ports'], host_result['last_update']])
		except:
			print("[-] We got an error here!")
			exit(1)			

	print(table)
