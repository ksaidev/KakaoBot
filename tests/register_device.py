from kakaopy.httpApi import RequestPasscode, RegisterDevice
from .settings import USER_ID, USER_PW, DEVICE_NAME, DEVICE_UUID

def register():
    """
    Registers the virtual device in your KakaoTalk account
    Should be runned initialy before running main script
    """
    RequestPasscode(USER_ID, USER_PW, DEVICE_NAME, DEVICE_UUID)

    print("Please check your phone or computer for the authorization passcode")
    passcode = str(input("PASSCODE : "))

    RegisterDevice(USER_ID, USER_PW, DEVICE_NAME, DEVICE_UUID, passcode)


if __name__ == '__main__':
    # Can also registered by running this code independently
    register()
