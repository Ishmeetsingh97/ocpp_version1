import asyncio
import websockets
from client import messageSelection
from pymongo import MongoClient
import jsons
import os
import time

mongoClient = MongoClient('localhost', 27017)
dbObject = mongoClient['ev_db']
info = dbObject.ev_data


# BootNotification,SingleSocketCar,VendorX,PowerUp

async def message():
    async with websockets.connect("ws://localhost:9000", subprotocols=['ocpp2.0.1']) as socket:
        while True:
            request_to_server = await ask_payload_loop()
            await socket.send(jsons.dumps(request_to_server))
            await db_operations(request_to_server)
            response_from_server = await socket.recv()
            print(response_from_server)


async def db_operations(request):
    request = {"request": request}
    info.insert_one(request)


async def ask_payload_loop():
    request = await ask_payload()
    while request == "NULL":
        request = await ask_payload()
    return request


async def ask_payload():
    msg = await check_size()
    request = await ask_payload_data(msg)
    return request


async def check_size():
    file_size = os.path.getsize("input_data.txt")
    if file_size == 0:
        time.sleep(30)
        return "NULL"
    else:
        file = open("input_data.txt", "r+")
        msg = file.read()
        msg = msg.strip('\n')
        msg = str.split(msg, sep=",")
        file.truncate(0)
        return msg


async def ask_payload_data(msg):
    switcher = {
        'quit': lambda: messageSelection.stopping_condition_request(),
        'BootNotification': lambda: messageSelection.boot_notification_request(msg)
    }
    func = switcher.get(msg[0], lambda: messageSelection.invalid_response())
    return func()


if __name__ == '__main__':
    asyncio.run(message())
