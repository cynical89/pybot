import time
import event
import json
from slackclient import SlackClient

json_data = open('config.json').read()
data = json.loads(json_data)


class Bot(object):
    def __init__(self):
        self.slack_client = SlackClient(data['api_keys']['slack'])
        self.bot_name = 'pybot'
        self.bot_id = self.get_bot_id()

        if self.bot_id is None:
            exit('Error, could not find {}'.format(self.bot_name))

        self.event = event.Event(self)
        self.listen()

    def get_bot_id(self):
        api_call = self.slack_client.api_call('users.list')
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    return '<@{}>'.format(user.get('id'))

            return None

    def listen(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print("Successfully connected to slack! Listening..")
            while True:
                self.event.wait_for_event()

                time.sleep(1)
        else:
            exit("Error, could not connect")
