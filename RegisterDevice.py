import httpLogin

user_id=str(input("ID: "))
user_pw=str(input("PW: "))

device_name="DEVICE"
user_uuid="REVWSUNFMQ=="

RequestPasscode(user_id, user_pw,
               device_name, user_uuid)

passcode=str(input("Input Passcode : "))

RegisterDevice(user_id, user_pw,
               device_name, user_uuid, passcode)
