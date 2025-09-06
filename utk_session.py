# utk_session.py
import requests, json, time
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

KEY = b'%!$!%_$&!%F)&^!^'
IV  = b'#*y*#2yJ*#$wJv*v'

def decrypt(enc: str) -> str:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return unpad(cipher.decrypt(b64decode(enc)), AES.block_size).decode()

class UtkSession:
    def __init__(self):
        self.token   = None
        self.cookies = {}

    def login(self, uid: str, pwd: str) -> bool:
        # 1. CSRF token लो
        r = requests.get('https://online.utkarsh.com/web/home/get_states', timeout=30)
        self.token = r.json()['token']

        # 2. लॉगिन करो
        data = f"csrf_name={self.token}&mobile={uid}&url=0&password={pwd}&submit=LogIn&device_token=null"
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.post('https://online.utkarsh.com/web/Auth/login',
                          headers=headers, data=data, timeout=30)

        # 3. जवाब decrypt करो
        enc = r.json()['response'].replace('MDE2MTA4NjQxMDI3NDUxNQ==', '==').replace(':', '==')
        dec = json.loads(decrypt(enc))
        if dec.get('status'):
            self.cookies = dict(r.cookies)
            return True
        return False

    def headers(self):
        return {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'origin': 'https://online.utkarsh.com',
            'cookie': f'csrf_name={self.token}; ' + '; '.join(f'{k}={v}' for k, v in self.cookies.items())
        }
