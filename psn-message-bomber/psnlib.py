import json, requests, time, random

errors = {"loginfailed" : "0",
          "loginsuccess" : "1",
          "messagefailed" : "2",
          "messagesuccess" : "3"}

psnVars = { "SENBaseURL" : "https://auth.api.sonyentertainmentnetwork.com",
            "redirectURL_oauth" : "com.scee.psxandroid.scecompcall://redirect",
            "client_id" : "b0d0d7ad-bb99-4ab1-b25e-afa0c76577b0",
            "scope" : "sceapp",
            "scope_psn" : "psn:sceapp",
            "client_secret" : "Zo4y8eGIa3oazIEp",
            "duid" : "00000005006401283335353338373035333434333134313a433635303220202020202020202020202020202020",
            "cltm" : "1399637146935",
            "service_entity" : "urn:service-entity:psn",
            "useragent" : "Mozilla/5.0 (PLAYSTATION 3 4.21) AppleWebKit/531.22.8 (KHTML, like Gecko)"}

psnURLS = { "signIn" : psnVars["SENBaseURL"] + "/2.0/oauth/authorize?response_type=code&service_entity=" + psnVars["service_entity"] + "&returnAuthCode=true&cltm=" + psnVars["cltm"] + "&redirect_uri=" + psnVars["redirectURL_oauth"] + "&client_id=" + psnVars["client_id"] + "&scope=" + psnVars["scope_psn"],
            "signInPost" : psnVars["SENBaseURL"] + "/login.do",
            "oauth" : "https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/token",

            "friendlistURL" : "https://{{region}}-prof.np.community.playstation.net/userProfile/v1/users/{{id}}/friendList?fields=onlineId,avatarUrl,plus,personalDetail,trophySummary&friendStatus=friend",
            "profileData" : "https://{{region}}-prof.np.community.playstation.net/userProfile/v1/users/{{id}}/profile?fields=@default,relation,requestMessageFlag,presence,@personalDetail,trophySummary",
            "onlineState" : "https://{{region}}-prof.np.community.playstation.net/userProfile/v1/users/{{id}}/profile?fields=presence",

            "trophyData" : "https://{{region}}-tpy.np.community.playstation.net/trophy/v1/trophyTitles?fields=@default&npLanguage={{lang}}&iconSize={{iconsize}}&platform=PS3,PSVITA,PS4&offset={{offset}}&limit={{limit}}",
            "trophyDataList" : "https://{{region}}-tpy.np.community.playstation.net/trophy/v1/trophyTitles/{{npCommunicationId}}/trophyGroups/{{groupId}}/trophies?fields=@default,trophyRare,trophyEarnedRate&npLanguage={{lang}}",
            "trophyGroupList" : "https://{{region}}-tpy.np.community.playstation.net/trophy/v1/trophyTitles/{{npCommunicationId}}/trophyGroups/?npLanguage={{lang}}",
            "trophyInfo" : "https://{{region}}-tpy.np.community.playstation.net/trophy/v1/trophyTitles/{{npCommunicationId}}/trophyGroups/{{groupId}}/trophies/{{trophyID}}?fields=@default,trophyRare,trophyEarnedRate&npLanguage={{lang}}",
            
            "conversations" : "https://{{region}}-gmsg.np.community.playstation.net/groupMessaging/v1/users/{{id}}/messageGroups?fields=@default,messageGroupId,messageGroupDetail,totalUnseenMessages,totalMessages,latestMessage&npLanguage={{lang}}",
            "chat" : "https://{{region}}-gmsg.np.community.playstation.net/groupMessaging/v1/messageGroups/{{chatId}}/messages?fields=@default,messageGroup,body&npLanguage={{lang}}",
            "message" : "https://{{region}}-gmsg.np.community.playstation.net/groupMessaging/v1/messageGroups/{{chatId}}/messages" }

def login(email, password):
    s = requests.Session()

    # Login
    r = s.get(psnURLS["signIn"])

    headers = { "Origin" : "https://auth.api.sonyentertainmentnetwork.com",
                "Referer" : r.url }

    payload = { "j_username" : email,
                "j_password" : password,
                "params" : "service_entity=psn" }

    while True:
        try:
            r = s.post(psnURLS["signInPost"], data=payload, headers=headers)
        
            if "authentication_error=true" in r.url:
                return False

            authCode = r.url.split("authCode%3D")[1].split("&")[0]

            break
        except:
            if "loginSuccess.jsp" in r.url or "edit-profile!" in r.url:
                return

    # Get Access Token
    payload = { "grant_type" : "authorization_code",
                "client_id" : psnVars["client_id"],
                "client_secret" : psnVars["client_secret"],
                "code" : authCode,
                "redirect_uri" : psnVars["redirectURL_oauth"],
                "state" : "x",
                "scope" : psnVars["scope_psn"],
                "duid" : psnVars["duid"] }

    r = s.post(psnURLS["oauth"], data=payload)

    return json.loads(r.text)

def getMyInfos(accessToken):
    headers = { "Access-Control-Request-Method" : "GET",
                "Accept-Language" : "en-US,en;q=0.8",
                "X-NP-ACCESS-TOKEN" : accessToken,
                "User-Agent" : psnVars["useragent"] }
    
    r = requests.get("https://vl.api.np.km.playstation.net/vl/api/v1/mobile/users/me/info", headers=headers)
    return json.loads(r.text)

def sendMessage(accessToken, from_, to, message):
    messageURL = psnURLS["message"].replace("{{chatId}}", "~" + from_ + "," + to)

    data = {
             "message" : {
                         "messageKind" : 1,
                         "fakeMessageUid" : str(int(time.time())) + str(random.randint(100, 999)),
                         "body" : message.decode('cp1252').encode('utf-8')
                       }            
           }

    headers = {
                "Access-Control-Request-Method" : "POST",
                "Origin" : "http://psapp.dl.playstation.net",
                "Access-Control-Request-Headers" : "Origin, Accept-Language, Authorization, Content-Type, Cache-Control",
                "Accept-Language" : "en-US,en;q=0.8",
                "Authorization" : "Bearer " + accessToken,
                "Cache-Control" : "no-cache",
                "Accept-Encoding" : "gzip, deflate",
                "User-Agent" : psnVars["useragent"],
                "Content-Type" : "multipart/mixed; boundary=\"abcdefghijklmnopqrstuvwxyz\"" }
    
    payload = "--abcdefghijklmnopqrstuvwxyz\nContent-Type: application/json; charset=utf-8\nContent-Description: message\n\n" + json.dumps(data) + "\n--abcdefghijklmnopqrstuvwxyz--"

    r = requests.post(messageURL, data=payload, headers=headers)
    return json.loads(r.text)