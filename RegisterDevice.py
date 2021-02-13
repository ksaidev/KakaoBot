import httpApi

user_id = str(input("ID: "))
user_pw = str(input("PW: "))
device_name = "DEVICE"
user_uuid = "REVWSUNFMQ=="  # TODO what's the meaning?

httpApi.RequestPasscode(user_id, user_pw, device_name, user_uuid)

print("Please check your phone or computer for the authorization passcode")

passcode = str(input("Input Passcode : "))

httpApi.RegisterDevice(user_id, user_pw, device_name, user_uuid, passcode)
