#!/usr/bin/env python3

import constants
import urllib.parse
import requests
import json

class GitHub:

# supported: issues, pulls, comments

    def __init__(self, **kwargs):
        self.owner = kwargs['owner']
        self.repositories = kwargs['repositories']
        self.resources = kwargs['resources']   
        self.validate_resources()

        self.data_generator = self.data_generator()

    def validate_resources(self):
        for resource in self.resources:
            if resource not in constants.VALID_RESOURCES:
                raise Exception(resource + ' is not a supported resource!')

    def data_generator(self):
        for repository in self.repositories:
            for resource in self.resources:
                request_address = constants.GITHUB_API + constants.GITHUB_API_REPOS + self.owner + '/' + repository + '/' + resource                
                has_next = True
                while has_next:
                    request_response = requests.get(request_address)
                    yield request_response.json()
                    if 'next' in request_response.links:
                        request_address = request_response.links['next']['url']
                    else:
                        has_next = False
        print('reached this point')
        yield None

    def read(self):
        return next(self.data_generator)

if __name__ == "__main__":
    # gh = GitHub(owner='scrapinghub', repositories=['frontera'], resources=['issues','pulls','comments'])
    gh = GitHub(owner='scrapinghub', repositories=['frontera'], resources=['issues'])

    data1 = gh.read()
    for item in data1:
        print(item['id'])
    print('nextbatch')
    data2 = gh.read()
    for item in data2:
        print(item['id'])
    print('nextbatch')
    data3 = gh.read()
    for item in data3:
        print(item['id'])

