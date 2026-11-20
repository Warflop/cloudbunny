from __future__ import print_function
from urllib.parse import urlsplit
from censys.search import CensysCerts
from censys.search import CensysHosts
import configparser
import re
import math
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "api.conf"))

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
        api = CensysHosts(api_id = UID, api_secret = TOKEN)
        query_text = f'services.http.response.html_title: "{title}"'
        query = api.search(query_text)

        title_result = []
        for page in query:
            for host in page:
                title_result.append(host['ip'])

        if len(title_result) > 0:
            return set(title_result)
    except Exception as ex:
        print(ex)

'''The problem with this function is there is often too much data coming back.
    A search to a local univerity returned over 500 results!  
    I have broken it down in chunks and give the user an options of how many they want to return.  
    It seems anything over 10 will cause it to time out.  Even 10 is slow to go through.'''
def censys_search_certs(host, pg, mr):
    try:
        certificates = CensysCerts(api_id = UID, api_secret = TOKEN)
        query = f"parsed.names: {host} AND tags.raw: trusted AND NOT parsed.names: cloudflaressl.com"
        pages = -1 if mr == 0 else pg - 1 + math.ceil(mr / 50)
        cert_query = certificates.search(query, per_page = 50, pages = pages)

        cert_results = []
        for page_number, page in enumerate(cert_query, start = 1):
            if page_number < pg:
                continue
            cert_results.extend(page)
            if mr > 0 and len(cert_results) >= mr:
                break

        if mr > 0:
            cert_results = cert_results[:mr]
        results = set([cert['parsed.fingerprint_sha256'] for cert in cert_results])
        rc = len(results)
        if rc > 0:
            result_list = [result for result in results]
            hosts_query = CensysHosts(api_id = UID, api_secret = TOKEN)
            
            results_chunked = []
            if rc > 10:
                for i in range(0, math.ceil(10 * math.ceil(rc/10)), 10):
                    results_chunked.append(result_list[i:(i+10)])
            else:
                results_chunked.append(result_list[0:11])

            host_result = []
            for result_chunk in results_chunked:
                hosts = ' OR '.join(result_chunk)

                searching = hosts_query.search(hosts)

                for page in searching:
                    for search_result in page:
                        host_result.append(search_result['ip'])

            return set(host_result)
    except Exception as ex:
        print(ex)