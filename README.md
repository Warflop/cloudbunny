# CloudBunny 2.0

# UPDATE: NEW IN CLOUDBUNNY 2.0

* Fixed issues with running the code.
* Added page and result number options for Censys search. (1)
* Along with the ability to just search by certificate or by title. 
* Added ability to authenticate with just your API key in Zoomeye.
* Added option for free account users on Shodan to search. (2)
* General code cleanup.
* Comming soon: the ability to read input files of domains list and save output to file.

(1) I made the number of certificate results an option because search usually produce a lot of
results.  A search of a local university returned over 1000. The problem is the certificates are
then put into a Censys host search.  Anything over 10 seems to time out the server.  If the user wants 
to do over 10, then the certificates are passed through in chunks of 10.  So, there are multiple searches performed.<br />

(2) Free account user are not allowed to search with filters on the Shodan API (e.g. Title: "Some site").
For free users, the program will search unfilted (e.g. "Some Site").  Since this could produce false positives, I 
have included a warning message allowing the user to back out of the Shodan search.

# Summary

CloudBunny is a tool to capture the origin server that uses a WAF as a proxy or protection.

You can read more about the tool here: https://tinyurl.com/y8p48wb3

<p align="center">
<img src="https://i.imgur.com/CyGo02V.gif">
</p>

# Setup

In this tool, we use three search engines to search domain information: Shodan, Censys and Zoomeye.  To use this program, you need an API Key from one of the three services. (Don't worry all have free accounts :D ) You can find the API keys at the following links:

<pre>
<b>Shodan</b> - https://account.shodan.io/
<b>Censys</b> - https://censys.io/account/api
<b>ZoomEye</b> - https://www.zoomeye.org/profile
</pre>

After that you need to put the credentials in the <b>api.conf</b> file.

<b>NOTE</b>: In Zoomeye, for api.conf, you can either: enter your username and password OR your api key.  You only need one.

Install the requirements:

<pre>
$ pip3 install -r requirements.txt
</pre>

# Usage

After you have loaded your credentials and installed the requirements, execute:

<pre>
$ python3 cloudbunny.py -u securityattack.com.br
</pre>

<i>Note: defaults are: search with all three search engines, 
perform both a certificate and title search with Censys, and limit Censys certificate results to 10.
This can be altered via command line switchrd.  See below.</i>

To search with just Shodan.io:

<pre>
$ python cloudbunny.py -u somesite.com -s
</pre>

To search Censys with the defaults:

<pre>
$ python cloudbunny.py -u somesite.com -c
</pre>

To search Censys with more records:

<pre>
#grabs first 50 results
$ python cloudbunny.py -u somesite.com -ccr 50
</pre>

To search Censys certificates with 20 results starting with the 7th page:

<pre>
$ python cloudbunny.py -u somesite.com -ccr 20 -ccp 7
</pre>

To search all Censys certificates:

<pre>
$ python cloudbunny.py -u somesite.com -ccr 0
</pre>

To search only Censys with title:

<pre>
$ python cloudbunny.py -u somesite.com -cc
</pre>

Check our help area:

<pre>
$ python3 cloudbunny.py -h
</pre>

Change <b>securityattack.com.br</b> for the domain of your choice.

# Example

<pre>
$ python cloudbunny.py -u testphp.vulnweb.com
 
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
    
[+] Looking for target on Shodan...
[*] It looks like you're on the free account.
In order to search with filters you will need to upgrade.
The best we can do is give you a filterless search for the title.
This does increase the chances of false positives.
Still want to continue with this part of the search? (Y/N):
Y
[+] Looking for target on Censys...
[+] Looking for certificates on Censys...
[+] Looking for target on ZoomEye...
[*] We found some data. Give us a moment to print it out...

No information available for that IP.
No information available for that IP.
+-------------+------------------+----------------+----------------------------+
|  IP Address |       ISP        |     Ports      |        Last Update         |
+-------------+------------------+----------------+----------------------------+
| 13.230.9.13 | Amazon.com, Inc. | [80, 8080, 22] | 2022-01-28T03:08:59.580527 |
+-------------+------------------+----------------+----------------------------+
+---------------+------------------+----------------+----------------------------+
|   IP Address  |       ISP        |     Ports      |        Last Update         |
+---------------+------------------+----------------+----------------------------+
|  13.230.9.13  | Amazon.com, Inc. | [80, 8080, 22] | 2022-01-28T03:08:59.580527 |
| 52.203.56.158 | Amazon.com, Inc. |   [80, 443]    | 2022-01-26T12:41:45.460829 |
+---------------+------------------+----------------+----------------------------+
+----------------+-----------------------+----------------+----------------------------+
|   IP Address   |          ISP          |     Ports      |        Last Update         |
+----------------+-----------------------+----------------+----------------------------+
|  13.230.9.13   |    Amazon.com, Inc.   | [80, 8080, 22] | 2022-01-28T03:08:59.580527 |
| 52.203.56.158  |    Amazon.com, Inc.   |   [80, 443]    | 2022-01-26T12:41:45.460829 |
| 51.116.130.248 | Microsoft Corporation |    [27017]     | 2022-01-28T06:40:05.143317 |
+----------------+-----------------------+----------------+----------------------------+
 

  /\=//\-"""-.        
 / /6 6\ \     \        
  =\_Y_/=  (_  ;{}     
    /^//_/-/__/      
    "" ""  """       
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    We may have some false positives :)
</pre>
