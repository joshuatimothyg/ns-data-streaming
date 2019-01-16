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

        self.validate_owner()   
        self.validate_repositories()
        self.validate_resources()

        self.data_generator = self.data_generator()

    def validate_owner(self):
        request_address = constants.GITHUB_API + constants.GITHUB_API_USERS + self.owner
        request_response = requests.get(request_address)
        if not(request_response.ok):
            raise Exception(self.owner + ' is not a valid owner!')

    def validate_repositories(self):
        for repository in self.repositories:
            request_address = constants.GITHUB_API + constants.GITHUB_API_REPOS + self.owner + '/' + repository
            request_response = requests.get(request_address)
            if not(request_response.ok):
                raise Exception(repository + ' is not a valid repository!')

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
                    print(repository + ' -> ' + resource)
                    request_response = requests.get(request_address)
                    json_response = request_response.json()
                    if json_response:
                        if 'next' in request_response.links:
                            print('entering next')
                            request_address = request_response.links['next']['url']
                        else:
                            has_next = False
                        yield json_response
                    else:
                        has_next = False
        print('reached this point')
        yield None

    def read(self):
        return next(self.data_generator)

if __name__ == "__main__":
    gh = GitHub(owner='scrapinghub', repositories=['frontera','hubris'], resources=['issues','pulls','comments'])
    # gh = GitHub(owner='joshuatimothyg', repositories=['chiffon-problems'], resources=['issues'])

    data = gh.read()
    while data is not None:
        for item in data:
            print(item['id'])
        print('-------nextbatch')
        data = gh.read()


