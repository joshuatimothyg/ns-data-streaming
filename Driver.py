#!/usr/bin/env python3

import GitHub

if __name__ == "__main__":
    gh = GitHub(owner='scrapinghub', repositories=['frontera','hubris'], resources=['issues','pulls','comments'])
    # gh = GitHub(owner='joshuatimothyg', repositories=['chiffon-problems'], resources=['issues'])

    data = gh.read()
    while data is not None:
        for item in data:
            print(item['id'])
        print('-------nextbatch')
        data = gh.read()

