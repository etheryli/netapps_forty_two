#!/usr/bin/env python3

import tweepy
from gtts import gTTS
import os
import socket
import sys
from clientKeys import *

host = sys.argv[2]
port = sys.argv[4]
size = sys.argv[6]
hashtag = sys.argv[8]


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        process_tweet(status.text)
        process_username(api.get_user(status.user.id_str).screen_name)
        return False


def process_tweet(text):
        with open('tweets.txt', 'w') as tweet_file:
            tweet_file.write(text + '\n')


def process_username(username):
        with open('tweets.txt', 'a') as tweet_file:
            tweet_file.write(username)            


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

while True:
    print("[Checkpoint 03] Listening for Tweets that contain: " + hashtag)
    myStream.filter(track=[hashtag], async=False)

    file = open("tweets.txt", "r")
    twitStringList = file.read().split()
    file.close()
    user = twitStringList[-1]
    del twitStringList[-1]
    questionString = ""
    for x in twitStringList:
        if(x != hashtag):
            questionString = questionString + " " + x

    print("[Checkpoint 04] New Tweet:" + questionString + " | User: " + user)
    tts = gTTS(questionString, lang='en')
    tts.save("good.mp3")
    print("[Checkpoint 05] Speaking question parsed for only Alphanumeric and Space characters:" + questionString)
    os.system("mpg321 good.mp3")
    
    print("[Checkpoint 06] Connecting to " + host + " on port " + port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    print("[Checkpoint 08] Sending question:" + questionString)
    s.send(questionString)
    data = s.recv(size)
    s.close()
    print('[Checkpoint 14] Received answer: ', data)
