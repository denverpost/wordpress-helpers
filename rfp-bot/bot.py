#!/usr/bin/env python
import os
import time
from slackclient import SlackClient

BOT_NAME = 'rfp-bot'
BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"

slack_cliet = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def main():
    """
        """
    READ_WEBSOCKET_DELAY = 1

def get_bot_id():
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)

if __name__ == "__main__":
    main()
