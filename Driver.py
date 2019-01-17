#!/usr/bin/env python3

from GitHub import GitHub
from GitHubAuth import GitHubAuth


if __name__ == "__main__":

    print('username:')
    username = input()
    print('password:')
    password = input()

    ghauth = GitHubAuth(username=username, password=password)
    gh = GitHub(authentication=ghauth, owner='github', repositories=['training-kit','gh-ost'], resources=['issues','pulls','comments'])

    # usage example:
    #       - printing ids of all the elements
    data = gh.read()
    while data is not None:
        for item in data:
            print(item['id'])
        data = gh.read()

