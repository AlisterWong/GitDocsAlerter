#!/usr/bin/env python
"""Sends alerts to a Discord webhook based on GitHub text files

This program listens for alerts from GitHub webhooks to run (POST requests).
It then checks if there were any commits and collects the names of unique
'.md' files and attempts to send a Discord message with the contents of 
such files.
"""

import requests
from flask import Flask, request, Response
from discord_webhooks import DiscordWebhooks

__author__ = "Alister Wong"

__version__ = "1.0"
__maintainer__ = "Alister Wong"
__email__ = "alister64@live.com.au"

fwebhook = open("webhook.txt", "r")

# Webhook URL for your Discord channel.
WEBHOOK_URL = fwebhook.read().strip()

class message:

    def __init__(self, file):
        self.file = file
        
    def send_message(self):
        """ Sends an alert to discord with the contents of the file """
        # Initialize the webhook class and attaches data.
        webhook = DiscordWebhooks(WEBHOOK_URL)
        
        # Change this URL to change which repository to pull commits from.
        url = "https://api.github.com/repos/COMP30022-2022/COMP30022/contents/"
        url = url + self.file

        ftoken = open("token.txt", "r")
        
        header = "application/vnd.github.raw"
        token = ftoken.read().strip()

        # Verifies the github token
        resp = requests.get(url, headers={"Accept": header, "Authorization": "token " + token})
        
        if resp.ok:
            # Appends a field
            webhook.add_field(name=self.file, value=resp.text)

            # Triggers the payload to be sent to Discord.
            webhook.send()
        else:
            raise Exception("Github token invalid: " + self.file)


app = Flask(__name__)

# Setting route to respond to POST requests
@app.route('/webhook', methods=['POST'])
def return_response():
    """
    Finds unique filenames and creates a message object to send alerts via
    the send_message() function.
    """
    data = request.json
    # Can modify which file extensions to detect.
    file_extension = 'md'
    commit_set = set()

    # Goes through the commits and adds unique filenames to a set
    for commit in data["commits"]:
        for file in commit["added"]:
            if file.endswith(file_extension):
                commit_set.add(file)
        for file in commit["modified"]:
            if file.endswith(file_extension):
                commit_set.add(file)

    # Sends discord alert for each unique file in latest commit
    for item in commit_set:
        commit_message = message(item)
        commit_message.send_message()

    # Return successful response
    return Response(status=200)

if __name__ == "__main__": app.run(host='0.0.0.0', port=58372)
