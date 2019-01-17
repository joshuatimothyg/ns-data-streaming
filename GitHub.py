#!/usr/bin/env python3

import constants
import requests
import json

class GitHub:
    """ The GitHub class is able to retrieve data from the GitHub API and return it to the user in batches

    Attributes:
        authentication (obj) : object containing authentication login details
        owner          (str) : the user / org we want to fetch data from
        repositories   (list): the repositories we want to fetch data from
        resources      (list): the list of resources we want to retrieve / currently supported: issues, pulls, comments
        data_generator (func): generator function which can query the API and return data in batches
    """

    def __init__(self, **kwargs):
        self.authentication = kwargs['authentication']
        self.owner = kwargs['owner']
        self.repositories = kwargs['repositories']
        self.resources = kwargs['resources']

        self.validate_owner()   
        self.validate_repositories()
        self.validate_resources()

        self.data_generator = self.data_generator()

    def validate_owner(self):
        """ Validates if the owner entered by the user is valid """
        request_address = constants.GITHUB_API + constants.GITHUB_API_USERS + self.owner
        request_response = requests.get(request_address, auth=(self.authentication.username, self.authentication.password))
        if not(request_response.ok):
            raise Exception(self.owner + ' is not a valid owner!')

    def validate_repositories(self):
        """ Validates if the repositories entered by the user are valid """
        for repository in self.repositories:
            request_address = constants.GITHUB_API + constants.GITHUB_API_REPOS + self.owner + '/' + repository
            request_response = requests.get(request_address, auth=(self.authentication.username, self.authentication.password))
            if not(request_response.ok):
                raise Exception(repository + ' is not a valid repository!')

    def validate_resources(self):
        """ Validates if the resources entered by the user are valid and covered by the class"""
        for resource in self.resources:
            if resource not in constants.VALID_RESOURCES:
                raise Exception(resource + ' is not a supported resource!')

    def data_generator(self):
        """ Generator function which sends back data to the user in batches
        
        Returns:
            (list) the succeeding list of objects in the sequence
        """
        for repository in self.repositories:
            for resource in self.resources:
                request_address = constants.GITHUB_API + constants.GITHUB_API_REPOS + self.owner + '/' + repository + '/' + resource 
                has_next = True
                while has_next:
                    request_response = requests.get(request_address, auth=(self.authentication.username, self.authentication.password))
                    json_response = request_response.json()
                    if json_response:
                        if 'next' in request_response.links:
                            request_address = request_response.links['next']['url']
                        else:
                            has_next = False
                        yield json_response
                    else:
                        has_next = False
        yield None

    def read(self):
        """ Helper function which calls the data generator method
        
        Returns:
            (list) the succeeding list of objects in the sequence
        """
        return next(self.data_generator)
