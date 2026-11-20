from __future__ import print_function
import requests
import configparser
import urllib.parse
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "api.conf"))

username = config.get('zoomeye', 'username')
password = config.get('zoomeye', 'password')
apikey = config.get('zoomeye', 'token')

###TODO: this will work for someone who has a username and password, but you could also have your login tied to many sources.
###Give the user an option of using their API key instead.
def zoomeye_search(word):
	try:
		if not apikey:
			data = '{ "username": "' + username + '", "password": "' + password + '" }'
			response = requests.post('https://api.zoomeye.org/user/login', data = data)
			token = response.json()['access_token']
	except:
		print("[-] We got an error with your zoomeye credentials. (Check if zoomeye is down ¯\\_(ツ)_/¯)")
		return

	try:
		headers = {}
		if apikey:
			headers = { 'API-KEY': apikey }
		else:
			headers = { 'Authorization': f'JWT {token}' }
		
		#work around to get zoomeye to accept the query.
		urlword = urllib.parse.quote(word)
		paramstring = f'https://api.zoomeye.org/host/search?query=title:"{urlword}"'
		response = requests.get(paramstring, headers = headers)
		final = response.json()['matches']
		title_result = set([host['ip'] for host in final])
		if title_result:
			return title_result

	except Exception as ex:
		print(ex)
