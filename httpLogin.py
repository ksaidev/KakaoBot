import requests
import hashlib

Agent = "win32"
Lang = "ko"
Version = "3.1.1"
AppVersion = "3.1.1.2441"
OsVersion = "10.0"

AuthHeader = "{agent}/{version}/{lang}".format(
    agent=Agent, version=Version, lang=Lang)
AuthUserAgent = "KT/{version} Wd/{osVer} {lang}".format(
    version=Version, osVer=OsVersion, lang=Lang)

LoginUrl = "https://ac-sb-talk.kakao.com/win32/account/login.json"
RegisterDeviceUrl = "https://ac-sb-talk.kakao.com/win32/account/register_device.json"
RequestPasscodeUrl = "https://ac-sb-talk.kakao.com/win32/account/request_passcode.json"
MoreSettingUrl = "https://sb-talk.kakao.com/win32/account/more_settings.json?since={since}&lang={lang}".format(
    since=0, lang=Lang)


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
        "permanent": "true",
    })

    return r.content.decode()

def getXVC(email, device_uuid, isFull=False):
    hash = hashlib.sha512("HEATH|{}|DEMIAN|{}|{}".format(
        AuthUserAgent, email, device_uuid).encode("utf-8")).hexdigest()
    if(isFull):
        return hash
    return hash[0:16]