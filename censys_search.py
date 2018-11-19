#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from urlparse import urlsplit 
import censys.certificates
import ConfigParser
import censys.ipv4
import re

config = ConfigParser.ConfigParser()
config.read("api.conf")
TOKEN = config.get('censys', 'token')
UID = config.get('censys', 'uid')

def split_url(url):
    if re.match(r'http(s?)\:', url):
        parsed = urlsplit(url)
        return parsed.netloc
    else:
        return url

def censys_search(title):
    try:
        api = censys.ipv4.CensysIPv4(api_id=UID, api_secret=TOKEN)
        query = api.search('80.http.get.title: "{0}"'.format(title))
        title_result = set([host['ip'] for host in query])
        if title_result:
            return title_result
    except:
        print("[-] We got an error here, maybe with your credentials!")
        exit(1)


def censys_search_certs(host):
    try:
        certificates = censys.certificates.CensysCertificates(api_id=UID, api_secret=TOKEN)

        cert_query = certificates.search("parsed.names: {0} AND tags.raw: trusted AND NOT parsed.names: cloudflaressl.com".format(host))        
        result = set([cert['parsed.fingerprint_sha256'] for cert in cert_query])        
        hosts_query = censys.ipv4.CensysIPv4(api_id=UID, api_secret=TOKEN)
        hosts = ' OR '.join(result)
        if hosts:
            searching = hosts_query.search(hosts)
            host_result = set([ search_result['ip'] for search_result in searching ])
            return host_result
    except:
        print("[-] We got an error here, maybe with your credentials!")
        exit(1)