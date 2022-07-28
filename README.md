# GitDocsAlerter
### Dependencies
This program relies on the discord_webhooks module and Python Flask.

https://github.com/JamesIves/discord-webhooks

### What does it do?
This program sends alerts to Discord based on a Discord webhook URL.
It uses verification via a private token on GitHub to check specific respositories
and pulls '.md' files from the specified repository.

It then shows the contents of such '.md' files in discord whenever it is run by
an alert from a GitHub webhook.

### How to use it?
1. Create a webhook.txt file with your Discord webhook URL, choosing which channel to 
send it to.

2. Create a token.txt file with your private Github token key. (Do not share this token)

   Remember to not share these two links.

3. Run this script on a server and have the GitHub webhook directed to this server.

4. Enjoy the Discord alerts
