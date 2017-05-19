import os

for i in range(0,255):
        add = "192.168."+str(i)+".0-254"
        os.system("nmap -sn "+add)

