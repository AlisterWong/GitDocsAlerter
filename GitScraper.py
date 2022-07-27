from discord_webhooks import DiscordWebhooks
import urllib.request
import requests
from flask import Flask, request, Response
import json

fwebhook = open("webhook.txt", "r")

# Webhook URL for your Discord channel.
WEBHOOK_URL = fwebhook.read()

class message:

    def __init__(self, folder, file):
        self.folder = folder
        self.file = file
        
    def send_message(self):
        # Initialize the webhook class and attaches data.
        webhook = DiscordWebhooks(WEBHOOK_URL)
        
        url = "https://api.github.com/repos/AlisterWong/COMP30023_Project_2/contents/"
        url = url + self.folder + "/"
        url = url + self.file

        ftoken = open("token.txt", "r")
        
        header = "application/vnd.github.raw"
        token = ftoken.read()

        
        resp = requests.get(url, headers={"Accept": header, "Authorization": "token " + token})
        
        #print(resp.text)
        if resp.ok:
            # Sets some content for a basic message.
            #webhook.set_content(content=resp.text)
            
            # Appends a field
            webhook.add_field(name=self.file, value=resp.text)

            # Triggers the payload to be sent to Discord.
            webhook.send()

test_message = message("www", "index.html")

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def return_response():
    print(request.json)
    #json_file = json.loads(request.json)
    #print("\n\n\n" + json_file)
    #print(json_file["commits"]["id"])
    #test_message.send_message()
    return Response(status=200)


if __name__ == "__main__": app.run()
