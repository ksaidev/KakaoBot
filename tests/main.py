from .customClient import CustomClient
from .settings import USER_ID, USER_PW, DEVICE_NAME, DEVICE_UUID

def main():
    client = CustomClient(DEVICE_NAME, DEVICE_UUID)
    client.run(USER_ID, USER_PW)
