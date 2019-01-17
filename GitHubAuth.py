#!/usr/bin/env python3

class GitHubAuth:
    """ The GitHubAuth class stores login credentials for users of the GitHub class

    Attributes:
        username (str): username of the GitHub class user
        password (str): password of the GitHub class user
    """
    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']
