#!/usr/bin/env python

import sys
import requests

def paste(endpoint, content):
    r = requests.post(endpoint, data = { 'content': content })
    return r.headers['Location']

def main():
    endpoint = 'http://p.cavi.cc/api/paste'
    with sys.stdin as f:
        url = paste(endpoint, f.read())
    print url

if __name__ == '__main__':
    main()
