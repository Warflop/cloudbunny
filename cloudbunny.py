#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from bs4 import BeautifulSoup
from urlparse import urlsplit
from zoomeye_search import *
from shodan_search import *
from censys_search import *
from random import choice
import requests, cfscrape
import argparse
import re

# “Never underestimate the determination of a kid who is time-rich and cash-poor.”

def banner():

	color = ['\033[95m' , '\033[96m', '\033[36m' , '\033[94m' , '\033[92m' , '\033[93m' , '\033[91m']

	print(choice(color) + ''' 
               _                                  
              (`  ).                   _           
             (     ).              .:(`  )`.       
)           _(       '`.          :(   .    )      
        .=(`(      .   )     .--  `.  (    ) )      
       ((    (..__.:'-'   .+(   )   ` _`  ) )                 
`.     `(       ) )       (   .  )     (   )  ._   
  )      ` __.:'   )     (   (   ))     `-'.-(`  ) 
)  )  ( )       --'       `- __.'         :(      )) 
.-'  (_.'          .')                    `(    )  ))
                  (_  )                     ` __.:'    

	            /|      __  
	           / |   ,-~ /  
	          Y :|  //  /    
	          | jj /( .^  
	          >-"~"-v"  
	         /       Y    
	        jo  o    |  
	       ( ~T~     j   
	        >._-' _./   
	       /   "~"  |    
	      Y     _,  |      
	     /| ;-"~ _  l    
	    / l/ ,-"~    \  
	    \//\/      .- \  
	     Y        /    Y*  
	     l       I     ! 
	     ]\      _\    /"\ 
	    (" ~----( ~   Y.  )   
	~~~~~~~~~~~~~~~~~~~~~~~~~~    
CloudBunny - Bypass WAF with Search Engines 
Author: Eddy Oliveira (@Warflop)
https://github.com/Warflop \033[0m
    ''')

def banner_footer():

	color = ['\033[95m' , '\033[96m', '\033[36m' , '\033[94m' , '\033[92m' , '\033[93m' , '\033[91m']

	print(choice(color) + ''' 

  /\\=//\-"""-.        
 / /6 6\ \     \        
  =\_Y_/=  (_  ;{}     
    /^//_/-/__/      
    "" ""  """       
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    We may have some false positives :)
\033[0m
	''')

def search(url):

	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

	try:
		
		if not re.match(r'http(s?)\:', url):
			url = 'http://' + url
			scraper = cfscrape.create_scraper()
			data  = scraper.get(url,headers=headers)
		else:
			scraper = cfscrape.create_scraper()
			data  = scraper.get(url,headers=headers)
		
	except:

		print("Hey buddy, pass a real address please!")
		exit(1)
		return
	
	if data.status_code == 200:
		soup = BeautifulSoup(data.text,'html.parser')
		for link in soup.title:
		    return link
	else:
		print("We had a problem with the URL!")
		exit(1)

def main():

	resolver = []
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", '--url', help="Hey buddy, can you give me the URL to test?")
	parser.add_argument("-s", '--shodan', action="store_true", help="Use Shodan")
	parser.add_argument("-c", '--censys', action="store_true", help="Use Censys")
	parser.add_argument("-z", '--zoomeye', action="store_true", help="Use ZoomEye")
	args = parser.parse_args()
	title =	search(args.url).encode('utf-8')
	host = split_url(args.url)

	if args.shodan or args.censys or args.zoomeye:

		if args.shodan:
			banner()
			print("[+] Looking for target on Shodan...")
			if not shodan_search(title) is None:
				for shodan_target in shodan_search(title):
					if not shodan_target in resolver:
						resolver.append(shodan_target)

		if args.censys:
			print("[+] Looking for target on Censys...")
			if not censys_search(title) is None:
				for censys_target in censys_search(title):
					if not censys_target in resolver:
						resolver.append(censys_target)
		
			print("[+] Looking for certificates on Censys...")
			if not censys_search_certs(host) is None:
				for censys_target_cert in censys_search_certs(host):
					if not censys_target_cert in resolver:
						resolver.append(censys_target_cert)

		if args.zoomeye:
			print("[+] Looking for target on ZoomEye...")
			if not zoomeye_search(title) is None:
				for zoomeye_target in zoomeye_search(title):
					if not zoomeye_target in resolver:
						resolver.append(zoomeye_target)

		if resolver:
			print("[*] We found some data wait just one more second...")
			print("\n")
			result_search(resolver)
		else:
			print("\n")
			print("[-] Looks like our rabbit has not gotten so deep. :(")

		banner_footer()

	else:
			banner()
			print("[+] Looking for target on Shodan...")
			if not shodan_search(title) is None:
				for shodan_target in shodan_search(title):
					if not shodan_target in resolver:
						resolver.append(shodan_target)

			print("[+] Looking for target on Censys...")
			if not censys_search(title) is None:
				for censys_target in censys_search(title):
					if not censys_target in resolver:
						resolver.append(censys_target)
		
			print("[+] Looking for certificates on Censys...")
			if not censys_search_certs(host) is None:
				for censys_target_cert in censys_search_certs(host):
					if not censys_target_cert in resolver:
						resolver.append(censys_target_cert)

			print("[+] Looking for target on ZoomEye...")
			if not zoomeye_search(title) is None:
				for zoomeye_target in zoomeye_search(title):
					if not zoomeye_target in resolver:
						resolver.append(zoomeye_target)

			if resolver:
				print("[-] Just more some seconds...")
				print("\n")
				result_search(resolver)
			else:
				print("\n")
				print("[-] Looks like our rabbit has not gotten so deep. :(")

			banner_footer()

if __name__ == '__main__':
    main()
