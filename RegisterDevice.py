import httpApi

user_id=str(input("ID: "))
user_pw=str(input("PW: "))

device_name="DEVICE"
user_uuid="REVWSUNFMQ=="

httpLogin.RequestPasscode(user_id, user_pw,
               device_name, user_uuid)

passcode=str(input("Input Passcode : "))

httpLogin.RegisterDevice(user_id, user_pw,
               device_name, user_uuid, passcode)
