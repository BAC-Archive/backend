import requests,json
url="http://127.0.0.1:5050/register"
user="anazwen"
passw="khaybnta"
data='{"user":"hi","pass":"passw"}'
# data=json.dumps(data)
grab=requests.post(url,data)
print(grab.text)