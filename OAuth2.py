import requests
import urllib
from requests.models import Response, codes
from selenium import webdriver
import chromedriver_binary

driver = webdriver.Chrome()
# 認証コードを取得する
auth_url = 'https://login.live.com/oauth20_authorize.srf'
client_id = '21b4672b-835f-4a01-8fa2-a34d39202601'
scope = 'offline_access onedrive.appfolder'
redirect_uri = 'https://login.microsoftonline.com/common/oauth2/nativeclient'
# response = requests.get('https://login.live.com/oauth20_authorize.srf',
#     params={
#       'client_id':client_id,
#       'scope':scope,
#       'redirect_uri':redirect_uri,
#       'response_type':'code',  
#     }
# )
# auth_params={
#     'client_id':client_id,
#     'scope':scope,
#     'redirect_uri':redirect_uri,
#     'response_type':'code',  
# }
# quety_params = urllib.parse.urlencode(auth_params)
# driver.get(auth_url+'?'+quety_params)
driver.quit()

# コードをアクセス トークンと交換する
client_secret = 'igy7Q~F9Id2_0AIt88GWMFP-.fOVV~Fira_VX'
code = 'M.R3_BAY.9decd17f-0a67-ffed-7a6a-d33d0c20394f'
token_params = {
    'client_id':client_id,
    'redirect_uri':redirect_uri,
    'client_secret':client_secret,
    'code':code,
    'grant_type':'authorization_code'
}
response = requests.post(auth_url,
                data=urllib.parse.urlencode(token_params)
            )
print(response.__dict__)