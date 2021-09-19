import requests

client_id = '21b4672b-835f-4a01-8fa2-a34d39202601'
redirect_uri = 'https://login.microsoftonline.com/common/oauth2/nativeclient'
get_url = f'https://login.live.com/oauth20_authorize.srf?response_type=code&client_id={client_id}&scope=wl.signin%20wl.skydrive&redirect_uri={redirect_uri}'
# r = requests.get(get_url)
auth_code = 'M.R3_BAY.59849e65-1bb3-8fe5-0cf2-69fd2aaa9218'
client_secret = 'MVB7Q~RHJPdlR0cpqZdv1fQrzD4ahgYgkk3U~'
responce = requests.post('https://login.live.com/oauth20_token.srf', data={
    # 'Content-Type':'application/x-www-form-urlencoded',
    # 'grant_type':f'authorization_code&code={auth_code}&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}'
    'client_id':client_id,
    'redirect_uri':redirect_uri,
    'client_secret':client_secret,
    'code':code,
    'grant_type':auth_code
})
print(responce.json())