import requests
import json

json_data = open('config.json').read()
data = json.loads(json_data)
yt_dev_key = data['api_keys']['youtube']
gif_dev_key = data['api_keys']['giphy']


yt_base_url = 'https://www.googleapis.com/youtube/v3/'
yt_search_api_url = yt_base_url + 'search?part=id&maxResults=1'
yt_video_url = "http://youtu.be/%s"

gif_base_url = 'https://api.giphy.com/v1/gifs/search?api_key='
gif_search_url = gif_base_url + '{}&q={}&limit=1&offset=0&rating=R&lang=en'


class Command(object):
    def __init__(self):
        self.commands = {
            "ping": self.ping,
            'yt': self.you_tube,
            'gif': self.giphy,
            "help": self.help
        }

    def handle_command(self, user, command, text):
        response = '<@{}>'.format(user)

        if command in self.commands:
            response += self.commands[command](text)
        else:
            response += (
                "Sorry, " + command + " is an unknown command. " + self.help())

        return response

    def ping(self):
        return 'pong!'

    def you_tube(self, text):
        response = requests.get(yt_search_api_url, params={
            'q': text, 'key': yt_dev_key, 'type': 'video'}).json()

        if response.get('error'):
            if response['error']['code'] == 403:
                return "Youtube Api is currently unavailable"
            else:
                return "There was an error searching"

        if response['pageInfo']['totalResults'] == 0:
            return "No results found"

        video_id = response['items'][0]['id']['videoId']

        return yt_video_url % video_id

    def giphy(self, text):
        print(gif_search_url.format(
            gif_dev_key, text))
        response = requests.get(gif_search_url.format(
            gif_dev_key, text)).json()

        if response.get('error'):
            if response['error']['code'] == 403:
                return "Giphy Api is currently unavailable"
            else:
                return "There was an error searching"

        if response['pagination']['count'] == 0:
            return "No results found"

        print(response['data'][0]['url'])
        return response['data'][0]['url']

    def help(self):
        response = 'Supported commands:\r\n'

        for command in self.commands:
            response += command + '\r\n'

        return response
