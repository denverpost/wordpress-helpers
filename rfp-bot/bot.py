#!/usr/bin/env python
import os
import time
from slackclient import SlackClient

BOT_NAME = 'rfp-bot'
BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def post_message(channel):
    """
        """
    # {u'text': u'<@U2KNVHM2P> aaaaaa', u'ts': u'1475698060.000016', u'user': u'U040B56RE', u'team': u'T0408FW33', u'type': u'message', u'channel': u'C2KPA2CUB'}
    response="HELLO AGAIN"
    channel="C2KPA2CUB"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def main():
    """
        """
    post_message('')
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("RFP-BOT is connected and running")
        while True:
            outputs = slack_client.rtm_read()
            if len(outputs) > 0:
                for output in outputs: 
                    print output
                    if hasattr(output, 'channel'):
                        print output
                        post_message(output['channel'])
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed")

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
