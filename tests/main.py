from kakaopy.httpApi import RequestPasscode, RegisterDevice
from .customClient import CustomClient

def main():
    check_registered = str(input("Have you already registered? (y/n) "))
    user_id = "your email"
    user_pw = "your password"
    device_name = "any string"
    user_uuid = 'REVWSUNFMQ=='  # TODO 되는 경우에 대한 규칙성 필요 => randomize 바꾸지 않는게 좋을 듯
    
    if check_registered == n:
        RequestPasscode(user_id, user_pw, device_name, user_uuid)

        print("Please check your phone or computer for the authorization passcode")
        passcode = str(input("PASSCODE : "))

        RegisterDevice(user_id, user_pw, device_name, user_uuid, passcode)

    client = CustomClient(device_name, user_uuid)
    client.run(user_id, user_pw)
