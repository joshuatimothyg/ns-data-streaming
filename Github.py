#!/usr/bin/env python3

import urllib.parse
import requests
import json

class GitHub:

    def __init__(self, **kwargs):
        self.owner = kwargs['owner']
        self.owner_type = self.get_user_type()
        self.repositories = kwargs['repositories']
        self.resources = kwargs['resources']

        self.base_address = 'https://api.github.com/' + self.owner_type + self.owner
        print(self.base_address)

    def get_user_type(self):
        user_types_dict = { 'User' : 'users/',
                            'Organization': 'orgs/' }

        base_address = 'https://api.github.com/search/users?q='
        request_address = base_address + self.owner

        json_result = requests.get(request_address).json()

        for item in json_result['items']:
            if(item['login'] == self.owner):
                return user_types_dict[item['type']]

        raise Exception('User ' + self.owner + ' not found!')

"""
    def read(self):
        

        for repository in self.repositories:
            for resource in self.resources:


        request_address = self.base_address + urllib.parse.urlencode({'page':self.page})
        print(request_address)
        json_data = requests.get(request_address).json()

        self.page += 1

        return json_data
"""

if __name__ == "__main__":
    gh = GitHub(owner='joshuatimothyg', repositories='', resources='')
    gh = GitHub(owner='scrapinghub', repositories='', resources='')
    gh = GitHub(owner='arden2', repositories='', resources='')

    #print(gh.read())

"""

data = gh.read()
while data is not None:
    # do something with the data
    data = gh.read() # fetch next batch
"""