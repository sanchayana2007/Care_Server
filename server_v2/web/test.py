import requests
url = "https://www.fast2sms.com/dev/bulk/V2"
payload = "sender_id=FSTSMS&message=test&language=english&route=p&numbers=9999999999,888888888"
headers = {
'authorization': "YOUR_AUTH_KEY",
'Content-Type': "application/x-www-form-urlencoded",
'Cache-Control': "no-cache",
}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)