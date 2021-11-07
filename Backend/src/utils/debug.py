import requests

class Debug():
    def __init__(self, DEBUG_WEBHOOK):
        self.webhook = DEBUG_WEBHOOK
    
    def print_webhook(self, input_):
        r = requests.post(self.webhook, data = {"username" : "debug",
        "content" : input_})
    

