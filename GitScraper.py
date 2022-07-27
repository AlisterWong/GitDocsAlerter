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
        
        url = "https://api.github.com/repos/COMP30022-2022/COMP30022/contents/"
        url = url + self.folder + "/"
        url = url + self.file

        ftoken = open("token.txt", "r")
        
        header = "application/vnd.github.raw"
        token = ftoken.read()

        resp = requests.get(url, headers={"Accept": header, "Authorization": "token " + token})
        
        if resp.ok:
            # Appends a field
            webhook.add_field(name=self.file, value=resp.text)

            # Triggers the payload to be sent to Discord.
            webhook.send()


app = Flask(__name__)

# Setting route to respond to POST requests
@app.route('/webhook', methods=['POST'])
def return_response():
    data = request.json
    
    commit_set = set()

    # Goes through the commits and adds unique filenames to a set
    for commit in data["commits"]:
        for file in commit["added"]:
            if file.endswith('.md'):
                commit_set.add(file)
        for file in commit["modified"]:
            if file.endswith('.md'):
                commit_set.add(file)

    # Sends discord alert for each unique file in latest commit
    for item in commit_set:
        commit_message = message("Documentation", item)
        commit_message.send_message()

    # Return successful response
    return Response(status=200)

if __name__ == "__main__": app.run()
