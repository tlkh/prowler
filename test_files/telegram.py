import sys
import time
import telepot
from telepot.loop import MessageLoop
import pyrebase

subbed = []

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id, "k")
    if msg['text'] == "sub":
       subbed.append(chat_id)
    print(subbed)
        
def stream_handler(message):
    if message["data"] != "None":
        try:
            for chat in subbed:
                bot.sendMessage(chat, "New data: " + str(message["data"]))
        except Exception as e:
            print(e)
            print("no subscribers")

TOKEN = ""

config = {
    "apiKey": "",
    "authDomain": "clusterscanner.firebaseio.com",
    "databaseURL": "https://clusterscanner.firebaseio.com",
    "storageBucket": "clusterscanner.appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("fake@fake.com", "totallyLegit")
db = firebase.database()  # reference to the database service
time.sleep(1)
stream = db.child("172").child("22").stream(stream_handler)

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
