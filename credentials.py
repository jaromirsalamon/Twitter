import json


class Credentials:
    def __init__(self, jsonConfig):
        conf = open(jsonConfig, 'r')
        self.auth = json.load(conf)

    def getConsumerKey(self):
        if ('consumer_key' in self.auth) and (self.auth['consumer_key'] is not None):
            return self.auth['consumer_key']
        else:
            return None

    def getConsumerSecret(self):
        if ('consumer_secret' in self.auth) and (self.auth['consumer_secret'] is not None):
            return self.auth['consumer_secret']
        else:
            return None

    def getAccessToken(self):
        if ('access_token' in self.auth) and (self.auth['access_token'] is not None):
            return self.auth['access_token']
        else:
            return None

    def getAccessTokenSecret(self):
        if ('access_token_secret' in self.auth) and (self.auth['access_token_secret'] is not None):
            return self.auth['access_token_secret']
        else:
            return None
