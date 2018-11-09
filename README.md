# CloudBunny

CloudBunny is a tool to capture the real IP of the server that uses a WAF as a proxy or protection.

<p align="center">
<img src="https://i.imgur.com/CyGo02V.gif">
</p>

# How works

In this tool we used three search engines to search domain information: Shodan, Censys and Zoomeye. To use the tools you need the API Keys, you can pick up the following links:

<pre>
<b>Shodan</b> - https://account.shodan.io/
<b>Censys</b> - https://censys.io/account/api
<b>ZoomEye</b> - https://www.zoomeye.org/profile
</pre>

<b>NOTE</b>: In Zoomeye you need to enter the login and password, it generates a dynamic api key and I already do this work for you. Just enter your login and password.

After that you need to put the credentials in the <b>api.conf</b> file.

Install the requirements:

<pre>
$ sudo pip install -r requirements.txt
</pre>

# How to use

By default the tool searches on all search engines (you can set this up by arguments), but you need to put the credentials as stated above. After you have loaded the credentials and installed the requirements, execute:

<pre>
$ python cloudbunny.py -u securityattack.com.br
</pre>

Check our help area:

<pre>
$ python cloudbunny.py -h
</pre>

Change <b>securityattack.com.br</b> for the domain of your choice.