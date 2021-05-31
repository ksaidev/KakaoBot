import json

import requests
import hashlib

AGENT = "win32"
LANG = "ko"
VERSION = "3.1.1"
APP_VERSION = "3.1.1.2441"
OS_VERSION = "10.0"

AUTH_HEADER = f"{AGENT}/{VERSION}/{LANG}"
UTH_USER_AGENT = f"KT/{VERSION} Wd/{OS_VERSION} {LANG}"

LOGIN_URL = "https://ac-sb-talk.kakao.com/win32/account/login.json"
REGISTER_DEVICE_URL = "https://ac-sb-talk.kakao.com/win32/account/register_device.json"
REQUEST_PASSCODE_URL = "https://ac-sb-talk.kakao.com/win32/account/request_passcode.json"
MORE_SETTINGS_URL = f"https://sb-talk.kakao.com/win32/account/more_settings.json?since={0}&lang={LANG}"
MEDIA_URL = "https://up-m.talk.kakao.com/upload"


def request_passcode(email, password, device_name, device_uuid):
    h = header(email, device_uuid)
    d = get_data(email, password, device_name, device_uuid)
    d['permanent'] = "true"
    d['once'] = "false"
    r = requests.post(REQUEST_PASSCODE_URL, headers=h, data=d)

    return r.content.decode()


def register_device(email, password, device_name, device_uuid, passcode):
    h = header(email, device_uuid)
    d = get_data(email, password, device_name, device_uuid)
    d['permanent'] = "true"
    d['once'] = "false"
    d['passcode'] = passcode
    r = requests.post(REGISTER_DEVICE_URL, headers=h, data=d)

    return r.content.decode()


def login(email, password, device_name, device_uuid):
    h = header(email, device_uuid)
    d = get_data(email, password, device_name, device_uuid)
    d['permanent'] = True
    d['forced'] = True
    r = requests.post(LOGIN_URL, headers=h, data=d)

    return r.content.decode()


def header(email, device_uuid):
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "A": AUTH_HEADER,
        "X-VC": get_XVC(email, device_uuid),
        "User-Agent": UTH_USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": LANG,
    }


def get_XVC(email, device_uuid, is_full=False):
    string = f"HEATH|{UTH_USER_AGENT}|DEMIAN|{email}|{device_uuid}".encode("utf-8")
    hash_str = hashlib.sha512(string).hexdigest()
    if is_full:
        return hash_str
    return hash_str[0:16]


def get_data(email, password, device_name, device_uuid):
    return {
        "email": email,
        "password": password,
        "device_name": device_name,
        "device_uuid": device_uuid,
        "os_version": OS_VERSION
    }


def upload(data, data_type, user_id):
    r = requests.post(MEDIA_URL,
                      headers={"A": AUTH_HEADER, },
                      data={"attachment_type": data_type,
                            "user_id": user_id, },
                      files={'attachment': data, })
    path = r.content.decode()
    key = path.replace('/talkm', "")
    url = "https://dn-m.talk.kakao.com"+path

    return path, key, url


def post_text(chat_id, li, text, notice, access_key, device_uuid):
    if li == 0:
        url = f"https://talkmoim-api.kakao.com/chats/{chat_id}/posts"
    else:
        url = f"https://open.kakao.com/moim/chats/{chat_id}/posts?link_id={li}"

    r = requests.post(url, headers={"A": AUTH_HEADER,
                                    "User-Agent": UTH_USER_AGENT,
                                    "Authorization": f"{access_key}-{device_uuid}",
                                    "Accept-Language": "ko"},
                      data={"content": json.dumps([{"text": text, "type": "text"}]),
                            "object_type": "TEXT", "notice": notice})

    print(r.content.decode())
