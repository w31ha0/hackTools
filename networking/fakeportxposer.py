import os,sys

with open(sys.argv[1]) as f:
       content=f.readlines()

for line in content:
        index = line.find('/')
        if index > 7 or index == -1:
            continue
        port = line[:index]
        print "Running nc on port "+port
        os.system('nc 192.168.8.139 '+port)
