import requests
import urllib
from requests.models import Response, codes
from selenium import webdriver
import chromedriver_binary

with requests.Session() as s:
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    # 認証コードを取得する
    auth_url = 'https://login.live.com/oauth20_authorize.srf'
    client_id = '21b4672b-835f-4a01-8fa2-a34d39202601'
    scope = 'offline_access onedrive.appfolder'
    redirect_uri = 'https://login.microsoftonline.com/common/oauth2/nativeclient'
    response = s.get('https://login.live.com/oauth20_authorize.srf',
        params={
        'client_id':client_id,
        'scope':scope,
        'redirect_uri':redirect_uri,
        'response_type':'code',  
        }
    )
    auth_params={
        'client_id':client_id,
        'scope':scope,
        'redirect_uri':redirect_uri,
        'response_type':'code',  
    }
    quety_params = urllib.parse.urlencode(auth_params)
    driver.get(auth_url+'?'+quety_params)

    # コードをアクセス トークンと交換する
    token_url = 'https://login.live.com/oauth20_token.srf'
    # client_secret = '4aaabed8-8d7e-4d7b-bfff-d153be62275b'
    # client_secret = 'igy7Q~F9Id2_0AIt88GWMFP-.fOVV~Fira_VX'
    code = input('code: ')
    token_params = {
        'client_id':client_id,
        'redirect_uri':redirect_uri,
        # 'client_secret':client_secret,
        'code':code,
        'grant_type':'authorization_code'
    }
    body=urllib.parse.urlencode(token_params)
    token_response = s.post(token_url,
                    headers={'Content-Type':'application/x-www-form-urlencoded'},
                    data=body
                ).json()
    print(token_response)
    driver.quit()

    # 認証されたユーザーが使用できる drive リソースを一覧表示する。
    api_end_point = 'https://api.onedrive.com/v1.0'
    my_drives = '/me/drives'
    headers = {
        'Authorization': f"{token_response['token_type']} {token_response['access_token']}"
    }
    drive_list_response = s.get(api_end_point + my_drives, headers=headers)
    print(drive_list_response.content)
