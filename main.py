from telethon.sync import TelegramClient
from datetime import datetime,timedelta
from dateutil.tz import tzlocal
import pandas as pd
import json
import time

global client 
global newClient
global ids    
global config
global offset_date_time

def updateDatetime():
    datetimestamp = int(offset_date_time.timestamp())
    config["telegram"]["datetime"] = str(datetimestamp)
    with open("config/config.json", "w") as jsonfile:
        myJSON = json.dump(config, jsonfile) # Writing to the file
        jsonfile.close()

def isViAvailable(message):
    if message == None or message == '':
        return False
    message = message.lower()
    # if len(message) <= 80 and len(message) > 3 and ('available' in message or 'open' in message or 'book' in message) and 'no ' not in message and 'not ' not in message and 'mute' not in message and 'discussion' not in message and len(message.strip().split()) > 1 and 'total messages' not in message and 'ni vi' not in message and 'warn' not in message and 'thank you' not in message  and 'cool' not in message and 'expect' not in message and 'expect' not in message and 'dm me' not in message and 'ping me' not in message and 'testing' not in message and 'f1_' not in message and 'please' not in message and 'dont' not in message and 'don\'t' not in message and 'jo vi' not in message and 'mo vi' not in message and 'bo vi' not in message and 'expect' not in message and 'unavailable' not in message and '?' not in message :
    #     return True
    if len(message) <= 80 and len(message) > 3 and 'no ' not in message and 'not ' not in message  and 'report' not in message and 'ban' not in message and 'block' not in message and 'bot' not in message and 'mute' not in message and 'discussion' not in message and len(message.strip().split()) > 1 and 'total messages' not in message and 'ni vi' not in message and 'warn' not in message and 'thank you' not in message  and 'cool' not in message and 'expect' not in message and 'dm me' not in message  and 'ping me' not in message and 'testing' not in message and 'f1_' not in message and 'please' not in message and 'dont' not in message and 'don\'t' not in message and 'jo vi' not in message and 'mo vi' not in message and 'bo vi' not in message and 'expect' not in message and 'unavailable' not in message and '?' not in message :
        return True
    return False

def sendMessage(message,datetimeString):
    message = message +'\n'+datetimeString
    client.send_message(config["telegram"]["sender_channel"],message)
    newClient.send_message(int(ids[0]),message)

def getMessages(client,chats):
    global offset_date_time
    new_offset = datetime.now()
    for chat in chats:
        print(chat + " : " + offset_date_time.strftime("%m/%d/%Y, %H:%M:%S") + " - " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        try:
            messages = client.iter_messages(chat, offset_date=offset_date_time.astimezone(),reverse=True)
            for message in messages:
                print(message.message)
                print(message.date.astimezone(tzlocal()))
                if(isViAvailable(message.message)):
                    sendMessage(message.message, message.date.astimezone(tzlocal()).strftime("%m/%d/%Y, %H:%M:%S") )
            offset_date_time = new_offset
            updateDatetime()
        except:
            newClient.send_message(int(ids[0]),"telegram messages error : " + offset_date_time.strftime("%m/%d/%Y, %H:%M:%S"))
            print("unable to fetch data for the given time range")
        

with open('config/config.json') as f:
    config = json.load(f)

api_id = config["telegram"]["api_id"]
api_hash = config["telegram"]["api_hash"]
phone = config["telegram"]["phone"]
chats = config["telegram"]["chats"]
ids = config["telegram"]["ids"]
bot_key = config["telegram"]["bot_key"]
offset_date_time = datetime.fromtimestamp(int(config["telegram"]["datetime"]))
client = TelegramClient(phone, api_id, api_hash)
client.start()
newClient = TelegramClient(bot_key, api_id, api_hash)
newClient.start()
print('connected')
i = 0
while True:
    try:
        getMessages(client,chats)
        time.sleep(30)
    except:
        newClient.send_message(int(ids[0]),"telegram scraping failed")
        break
    