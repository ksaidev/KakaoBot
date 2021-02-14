from kakaopy.httpApi import RequestPasscode, RegisterDevice
from .customClient import CustomClient

def main():
    user_id = str(input("ID : "))
    user_pw = str(input("PW : "))
    device_name = "KAKAOPY TEST"
    user_uuid = 'AA'  # TODO 되는 경우에 대한 규칙성 필요 => randomize

    RequestPasscode(user_id, user_pw, device_name, user_uuid)

    print("Please check your phone or computer for the authorization passcode")
    passcode = str(input("PASSCODE : "))
    RegisterDevice(user_id, user_pw, device_name, user_uuid, passcode)

    client = CustomClient(device_name, user_uuid)
    client.run(user_id, user_pw)
