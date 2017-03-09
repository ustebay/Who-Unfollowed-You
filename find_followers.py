#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
# project: Insight-Churn
# date: 25/02/2014
# author: Deniz Ustebay
# description: Get a list of IDs for followers of a public Twitter account 
              (maximum of 5000 followers, could be increased below)

              Need to add access_token_key, access_token_secret, 
              consumer_key, consumer_secret

              CORRECT USAGE: python find_followers.py userName > followers.txt
"""


import oauth2 as oauth
import urllib2 as urllib
import json
import sys


access_token_key = ""
access_token_secret = ""

consumer_key = ""
consumer_secret = ""

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchfollowers(user_name):
  url = "https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=" + user_name + "&count=5000"
  # increase count above if you'd like to get more followers 
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    followers = json.loads(line)
    if 'ids' not in followers:
        print 'private account'
    else:   
        follower_ids = followers['ids']
        print 'total no of followers: ', len(follower_ids)
        for i in range(len(follower_ids)):
            print follower_ids[i]

def usage():
    sys.stderr.write("CORRECT USAGE: python find_followers.py userName > followers.txt\n")

if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly two arguments
        usage()
        sys.exit(2)
    else:
    	user_name = sys.argv[1]   

    fetchfollowers(user_name)
