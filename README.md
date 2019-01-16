# GitHub Data Streamer

## Inputs
* owner - target user/org's username
* repositories - list of repositories you want to retrieve specific resources from
* resources - list of resources you want to retrieve
  * currently supported - issues, pulls, comments

## Outputs
Every call to read() should return a list of items structured as a Python dictionary.