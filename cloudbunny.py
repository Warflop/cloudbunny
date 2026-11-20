from __future__ import print_function
from bs4 import BeautifulSoup
from zoomeye_search import *
from shodan_search import *
from censys_search import *
from random import choice
import cfscrape
import argparse
import re

def banner():

	color = ['\033[95m' , '\033[96m', '\033[36m' , '\033[94m' , '\033[92m' , '\033[93m' , '\033[91m']

	print(choice(color) + r'''
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
CloudBunny 2.0 - Bypass WAF with Search Engines 
V2 Author: Brian Wimpsett (@bwimpsett)
Author: Eddy Oliveira (@Warflop)
https://github.com/bwimpsett
https://github.com/Warflop
    ''' + '\033[0m')

def banner_footer():

	color = ['\033[95m' , '\033[96m', '\033[36m' , '\033[94m' , '\033[92m' , '\033[93m' , '\033[91m']

	print(choice(color) + r'''

  /\\=//\-"""-.        
 / /6 6\ \     \        
  =\_Y_/=  (_  ;{}     
    /^//_/-/__/      
    "" ""  """       
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    We may have some false positives :)
	''' + '\033[0m')

def search(url):

	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

	try:
		
		if not re.match(r'http(s?)\:', url):
			url = 'http://' + url
			scraper = cfscrape.create_scraper()
			data  = scraper.get(url,headers = headers)
		else:
			scraper = cfscrape.create_scraper()
			data  = scraper.get(url,headers = headers)
		
	except:
		print("[-] Hey buddy, pass a real address please!")
		exit(1)
	
	if data.status_code == 200:
		soup = BeautifulSoup(data.text,'html.parser')
		for link in soup.title:
			return link
	else:
		print("[-] We had a problem with the URL!")
		exit(1)

def main():
	banner()

	#TODO: Add I/O args.
	resolver = []
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", '--url', help = "Hey buddy, can you give me the URL to test?")
	parser.add_argument("-s", '--shodan', action = "store_true", help = "Use Shodan")
	parser.add_argument("-z", '--zoomeye', action = "store_true", help = "Use ZoomEye")
	
	parser.add_argument("-c", '--censys', action = "store_true", help = "Use Censys")
	parser.add_argument("-ct", action = "store_true", help = "Only title search in Censys.")
	
	parser.add_argument("-cc", action = "store_true", help = "Only certificate search in Censys.")
	parser.add_argument("-ccr", type = int, help = "Max number of certificate records to return from Censys (default: 10)")
	parser.add_argument("-ccp", type = int, help = "The page to start at for Censys certificate results (default: 1)")

	args = parser.parse_args()
	title =	search(args.url).encode('utf-8')
	host = split_url(args.url)
	noargs = not args.shodan and not args.censys and not args.zoomeye
	searchCensys = bool(args.censys or args.cc or args.ct or args.ccp or args.ccr)

	ccr = args.ccr
	if not ccr:
		ccr = 10

	ccp = args.ccp
	if not ccp:
		ccp = 1

	if args.shodan or args.censys or searchCensys or args.zoomeye or noargs:

		if args.shodan or noargs:
			print("[+] Looking for target on Shodan...")
			shodan_targets = shodan_search(title)
			if not shodan_targets is None:
				for shodan_target in shodan_targets:
					if not shodan_target in resolver:
						resolver.append(shodan_target)

		if searchCensys or noargs:
			if not args.cc:
				print("[+] Looking for target on Censys...")
				censys_targets = censys_search(title)
				censys_targets = None
				if not censys_targets is None:
					for censys_target in censys_targets:
						if not censys_target in resolver:
							resolver.append(censys_target)
			if not args.ct:
				print("[+] Looking for certificates on Censys...")
				censys_target_certs = censys_search_certs(host, ccp, ccr)
				if not censys_target_certs is None:
					for censys_target_cert in censys_target_certs:
						if not censys_target_cert in resolver:
							resolver.append(censys_target_cert)

		if args.zoomeye or noargs:
			print("[+] Looking for target on ZoomEye...")
			zoomeye_targets = zoomeye_search(title)
			if not zoomeye_targets is None:
				for zoomeye_target in zoomeye_targets:
					if not zoomeye_target in resolver:
						resolver.append(zoomeye_target)

		if resolver:
			print("[*] We found some data. Give us a moment to print it out...")
			print("\n")
			result_search(resolver)
		else:
			print("\n")
			print("[-] Looks like our rabbit has not gotten so deep. :(")

		banner_footer()

if __name__ == '__main__':
    main()
