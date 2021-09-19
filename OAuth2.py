import requests

client_id = '21b4672b-835f-4a01-8fa2-a34d39202601'
url = f'https://login.live.com/oauth20_authorize.srf?response_type=code&client_id={client_id}&scope=wl.signin%20wl.skydrive&redirect_uri=<redirect uri>'
r = requests.get(url)