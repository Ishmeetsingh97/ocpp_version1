import jsons
import uuid
from client import callRequest
from client.messageType import MessageType


def stopping_condition_request():
    quit()


def boot_notification_request(msg):
    model = msg[1]
    vendor_name = msg[2]
    reason = msg[3]

    request = callRequest.BootNotificationPayload(
        chargingStation={
            'model': model,
            'vendorName': vendor_name
        },
        reason=reason
    )

    request = jsons.load([MessageType.Call.value, str(uuid.uuid4()), msg[0], jsons.dump(request)], separators=(',', ':'))
    print(request)
    return request


def invalid_response():
    print("No valid request found, please try again!")
    return "NULL"
