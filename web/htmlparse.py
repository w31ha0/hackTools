from HTMLParser import HTMLParser

counter = 0
intr = False
types = []

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):		
    def handle_starttag(self, tag, attrs):
        if len(attrs) > 0:
            if attrs[0][0] == "lang":
                types.append(attrs[0][1])

    def handle_endtag(self, tag):
        pass
        
    def handle_data(self, data):
        pass
        
passwordfile = "html.txt"

with open(passwordfile) as f:
	contentp = f.read()

parser = MyHTMLParser()
parser.feed(contentp)
print "done"

f = open('languages.txt', 'w')
for content in types:
	print content
	f.write(content)
	f.write('\n')
f.close()