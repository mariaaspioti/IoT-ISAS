from smartcard.System import readers
from smartcard.util import toHexString
import time

last_uid = None

while True:
    try:
        # List all connected readers
        reader_list = readers()
        if not reader_list:
            time.sleep(1)
            continue

        reader = reader_list[0]
        connection = reader.createConnection()
        connection.connect()

        # Send command to get the UID
        get_uid_command = [0xFF, 0xCA, 0x00, 0x00, 0x00]
        response, sw1, sw2 = connection.transmit(get_uid_command)

        # Print the UID if a card is detected
        if sw1 == 0x90 and sw2 == 0x00:
            uid = toHexString(response)
            if uid != last_uid:
                print("UID:", uid)
                last_uid = uid
        else:
            last_uid = None

    except Exception as e:
        last_uid = None
        time.sleep(1)