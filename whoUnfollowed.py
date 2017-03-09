#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
# project: Insight-Churn
# date: 25/02/2014
# author: Deniz Ustebay
# description: Compare two lists of Twitter IDs, print out user names that are in the first file 
              but not in the second file. Each list can be generated using the find_followers.py file
              
              Need to add access_token_key, access_token_secret, consumer_key, consumer_secret

              USAGE TO GET UNFOLLOWERS: python whoUnfollowed.py followers_old followers_new
              USAGE TO GET NEW FOLLOWERS: python whoUnfollowed.py followers_new followers_old
              USAGE TO COMPARE TWO ACCOUNTS: python whoUnfollowed.py followers_userName1 followers_userName2
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

def read_ids(followers_file):
    ids = []
    l = followers_file.readline()
    while l:
        line = l.strip()
        if line: # Nonempty line
            fields = line.split(" ")
            if fields[0] != "total":
                ids.append(fields[0])
        l = followers_file.readline()
    return ids

def whoUnfollowed(followers_old, followers_new):
    old_ids = read_ids(followers_old)
    new_ids = read_ids(followers_new)
                
    for old_follower in old_ids:
        if old_follower not in new_ids:
            url = "https://api.twitter.com/1.1/users/show.json?user_id=" + str(old_follower) + "&include_entities=true"
            parameters = []
            response = twitterreq(url, "GET", parameters)
            for line in response:
                user = json.loads(line)
                if 'errors' in user:
                    print "unfollowed: user does not exist"
                else:
                    print "unfollowed: " + user["name"].encode('utf-8') + " @" + user["screen_name"].encode('utf-8')  
                    
                    
    for new_follower in new_ids:
        if new_follower not in old_ids:
            url = "https://api.twitter.com/1.1/users/show.json?user_id=" + str(new_follower) + "&include_entities=true"
            parameters = []
            response = twitterreq(url, "GET", parameters)
            for line in response:
                user = json.loads(line)
                print "new follower: " + user["name"].encode('utf-8') + " @" + user["screen_name"].encode('utf-8')    

                
                
    
def usage():
    sys.stderr.write("CORRECT USAGE: python whoUnfollowed.py followers_old followers_new \n")

if __name__ == "__main__":

    if len(sys.argv)!=3: # Expect exactly two arguments
        usage()
        sys.exit(2)
    try:
        followers_old = file(sys.argv[1],"r")
        followers_new = file(sys.argv[2],"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)    


    whoUnfollowed(followers_old, followers_new)
