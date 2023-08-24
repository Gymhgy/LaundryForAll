import random
import requests
from requests.structures import CaseInsensitiveDict
from requests import Request, Session

def register(api_key, email, token):
    s = Session()

    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json',
        'User-Agent': ""
    }

    json_data = {
        'sitecode': '000001',
        'password': 'qwerty1',
        'referring_uid': '',
        'app_type': '2',
        'location_code': 'D9999       ',
        'app_token': token,
        'email': email,
        'confirm_password': 'qwerty1',
    }

    resp = requests.post('https://digitalinsights.cscsw.com/api/auth/register_device_check', headers=headers, json=json_data)
    print(resp.headers)
    print(resp.json())

    if not resp.ok: raise SystemError

words = requests.get("https://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain", headers={"User-Agent": ""}).text.splitlines()

def generate_random_string(min_length, max_length):
    length = random.randint(min_length, max_length)
    characters = 'abcdefghijklmnopqrstuvwxyz123456789.'
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def generate_random_email(num_words):
    return ''.join([random.choice(words) for i in range(num_words)]).lower()

def get_api_key():
    url = "https://digitalinsights.cscsw.com/api/security/api_key"

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Basic YWRtaW46OTMxNQ=="
    headers["User-Agent"] = ""
    resp = requests.get(url, headers=headers)
    print(resp.json().get("api_key"))
    return resp.json().get("api_key")

api_key = get_api_key()

from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def home():
   return render_template('/index.html')

@app.route("/api/generate")
def generate():
    while True:
        email = generate_random_email(2) + f"@{generate_random_email(1)}.com"
        app_id = generate_random_string(5, 64)
        try:register(api_key, email, app_id)
        except SystemError:continue
        return email
    
if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)