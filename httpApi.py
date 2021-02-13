import json

import requests
import hashlib

agent = "win32"
lang = "ko"
version = "3.1.1"
appVersion = "3.1.1.2441"
osVersion = "10.0"

AuthHeader = f"{agent}/{version}/{lang}"
AuthUserAgent = f"KT/{version} Wd/{osVersion} {lang}"

LoginUrl = "https://ac-sb-talk.kakao.com/win32/account/login.json"
RegisterDeviceUrl = "https://ac-sb-talk.kakao.com/win32/account/register_device.json"
RequestPasscodeUrl = "https://ac-sb-talk.kakao.com/win32/account/request_passcode.json"
MoreSettingUrl = f"https://sb-talk.kakao.com/win32/account/more_settings.json?since={0}&lang={lang}"

MediaUrl = "https://up-m.talk.kakao.com/upload"


def RequestPasscode(email, password, device_name, device_uuid):
    r = requests.post(RequestPasscodeUrl, headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "A": AuthHeader,
        "X-VC": getXVC(email, device_uuid),
        "User-Agent": AuthUserAgent,
        "Accept": "*/*",
        "Accept-Language": Lang,
    }, data={
        "email": email,
        "password": password,
        "device_name": device_name,
        "device_uuid": device_uuid,
        "os_version": OsVersion,
        "permanent": "true",
        "once": "false",
    })

    return r.content.decode()


def RegisterDevice(email, password, device_name, device_uuid, passcode):
    r = requests.post(RegisterDeviceUrl, headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "A": AuthHeader,
        "X-VC": getXVC(email, device_uuid),
        "User-Agent": AuthUserAgent,
        "Accept": "*/*",
        "Accept-Language": Lang,
    }, data={
        "email": email,
        "password": password,
        "device_name": device_name,
        "device_uuid": device_uuid,
        "os_version": OsVersion,
        "permanent": "true",
        "once": "false",
        "passcode": passcode
    })

    return r.content.decode()


def Login(email, password, device_name, device_uuid):
    r = requests.post(LoginUrl, headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "A": AuthHeader,
        "X-VC": getXVC(email, device_uuid),
        "User-Agent": AuthUserAgent,
        "Accept": "*/*",
        "Accept-Language": Lang,
    }, data={
        "email": email,
        "password": password,
        "device_name": device_name,
        "device_uuid": device_uuid,
        "os_version": OsVersion,
        "permanent": True,
        "forced": True
    })

    return r.content.decode()


def upload(data, dataType, userId):
    r = requests.post(MediaUrl, headers={
        "A": AuthHeader,
    }, data={
        "attachment_type": dataType,
        "user_id": userId,
    }, files={
        'attachment': data,
    })
    path = r.content.decode()

    key = path.replace('/talkm', "")

    url = "https://dn-m.talk.kakao.com"+path

    return path, key, url


def postText(chatId, li, text, notice, accessKey, deviceUUID):
    if li == 0:
        url = f"https://talkmoim-api.kakao.com/chats/{chatId}/posts"
    else:
        url = f"https://open.kakao.com/moim/chats/{chatId}/posts?link_id={li}"
    print(requests.post(url,
                        headers={
                            "A": AuthHeader,
                            "User-Agent": AuthUserAgent,
                            "Authorization": f"{accessKey}-{deviceUUID}",
                            "Accept-Language": "ko"
                        }, data={
                            "content": json.dumps([{"text": text, "type": "text"}]),
                            "object_type": "TEXT",
                            "notice": notice
                        }).content.decode())


def getXVC(email, device_uuid, isFull=False):
    hash = hashlib.sha512(f"HEATH|{AuthUserAgent}|DEMIAN|{email}|{device_uuid}".encode("utf-8")).hexdigest()
    if(isFull):
        return hash
    return hash[0:16]
