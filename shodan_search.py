from __future__ import print_function
from itertools import count
from prettytable import PrettyTable
from shodan import Shodan
import configparser
import requests
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "api.conf"))

token = config.get('shodan', 'token')
api = Shodan(token)

def test_api_shodan(token):
	response = requests.get("https://api.shodan.io/api-info?key={0}".format(token))
	
	if response.status_code != 200:
		print("[-] We got an error with your shodan credentials.")
		return bool(0)
	return bool(1)

def shodan_search(word):
	if not test_api_shodan(token):
		return
	
	try:
		title_results = []
		userAccount = api.info()
		query = ''

		if userAccount['plan'] == 'oss':
			warnuser = '''
[*] It looks like you\'re on the free account.
In order to search with filters you will need to upgrade.
The best we can do is give you a filterless search for the title.
This does increase the chances of false positives.
Still want to continue with this part of the search? (Y/N):'''
			print(warnuser)
			
			confirmation = input()
			if confirmation.lower() == 'y' or confirmation.lower() == 'yes':
				query = word
			else:
				return
		else:
			query = 'http.title:"{0}"'.format(word)	

		result_count = api.count(query)['total']
		banner = api.search_cursor(query)
	
		'''for some reason shodan's api keeps going 
			and times out when I have finished looping through the results.'''
		if result_count > 0:
			acc = 0
			for host in banner:
				title_results.append(host['ip_str'])
				acc += 1
				if acc == result_count:
					break

		if len(title_results) > 0:
			return set(title_results)
	except Exception as ex:
		print(ex)

def result_search(list_host):
	table = PrettyTable(['IP Address','ISP','Ports','Last Update'])

	for check in list_host:
		try:
			host_result = api.host(check)
			table.add_row([host_result['ip_str'], host_result['isp'], host_result['ports'], host_result['last_update']])
			print(table)
		except Exception as ex:
			print(ex)
