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
        try:
            # 1. CSRF token लो
            r = requests.get('https://online.utkarsh.com/web/home/get_states', timeout=30)
            if r.status_code != 200:
                print("⚠️ CSRF Request Failed:", r.status_code, r.text)
                return False

            self.token = r.json().get('token')
            if not self.token:
                print("⚠️ CSRF Token missing in response:", r.text)
                return False

            # 2. लॉगिन करो
            data = f"csrf_name={self.token}&mobile={uid}&url=0&password={pwd}&submit=LogIn&device_token=null"
            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'x-requested-with': 'XMLHttpRequest',
                'origin': 'https://online.utkarsh.com',
                'referer': 'https://online.utkarsh.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }

            r = requests.post('https://online.utkarsh.com/web/Auth/login',
                              headers=headers, data=data, timeout=30)

            # Debug print (server ka raw response)
            print("🔎 RAW LOGIN RESPONSE:", r.text[:500])

            # 3. Agar response JSON nahi hai to fail
            try:
                resp = r.json()
            except Exception:
                print("❌ JSON parse failed. Response text:", r.text[:500])
                return False

            # 4. जवाब decrypt करो
            enc = resp.get('response', '')
            if not enc:
                print("⚠️ No encrypted response field found:", resp)
                return False

            enc = enc.replace('MDE2MTA4NjQxMDI3NDUxNQ==', '==').replace(':', '==')
            dec = json.loads(decrypt(enc))

            if dec.get('status'):
                self.cookies = dict(r.cookies)
                print("✅ Login Success!")
                return True
            else:
                print("❌ Login Failed:", dec)
                return False

        except Exception as e:
            print("🔥 Exception in login:", e)
            return False

    def headers(self):
        return {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'origin': 'https://online.utkarsh.com',
            'cookie': f'csrf_name={self.token}; ' + '; '.join(f'{k}={v}' for k, v in self.cookies.items())
        }
