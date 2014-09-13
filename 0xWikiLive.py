#!/usr/bin/python

import twitter;
from feedparser import parse;
import time;
import os;
import sys;

def init_tweet(ck, cs, atk, ats):
	api = twitter.Api(consumer_key=ck, consumer_secret=cs, access_token_key=atk, access_token_secret=ats);
	return api;

def send_tweet(api,tweet):
	try:
		status = api.PostUpdate(tweet);
	except:
		pass;
	print time.strftime("%d/%m/%y %H:%M:%S") + " : " + tweet;

def make_tweet(pseudo,item):
	return "@" + pseudo + " " + item.title + " - " + item.author + " (" + item.id + ")";

def get_entries(link):
	feed = parse(link);
	return feed;

def timestampisation(date):
	return time.mktime(time.strptime(date,"%Y-%m-%dT%H:%M:%SZ")) + (2*60*60);

def get_new_entries(link, old_timestamp):
	feed = get_entries(link);
	entries = [];
	for item in feed['entries']:
		if timestampisation(item.updated) > old_timestamp:
			entries.append(item);
	return entries;

def save_timestamp(timestamp):
	return 0;

def ask_args():
	print "The configuration file is missing. It will be generated.";
	print "\nConsumer key : ";
	print "> ", ; ck = sys.stdin.readline().split("\n")[0];
        print "\nConsumer secret : ";
        print "> ", ; cs = sys.stdin.readline().split("\n")[0];
        print "\nAccess token key : ";
        print "> ", ; atk = sys.stdin.readline().split("\n")[0];
        print "\nAccess token secret : ";
        print "> ", ; ats = sys.stdin.readline().split("\n")[0];
        print "\nLink to check : ";
        print "> ", ; link = sys.stdin.readline().split("\n")[0];
        print "\nTwitter account to notify : ";
        print "> ", ; pseudo = sys.stdin.readline().split("\n")[0];
        print "\nTime between 2 checks (in sec) : ";
        print "> ", ; wait = sys.stdin.readline().split("\n")[0];

	fichier = open("0xWikiLive.conf", "w");
	fichier.write(ck + "\n" + cs + "\n" + atk + "\n" + ats + "\n" + link + "\n" + pseudo + "\n" + wait);
	fichier.close();

	return ck, cs, atk, ats, link, pseudo, int(wait);

def get_args():
	if os.path.isfile("0xWikiLive.conf") == False:
		return ask_args();
	fichier = open("0xWikiLive.conf", "r");
	contenu = fichier.read();
	fichier.close();
	if len(contenu.split("\n")) < 7 or int(contenu.split("\n")[6]) < 1:
		return ask_args();
	return contenu.split("\n")[0], contenu.split("\n")[1], contenu.split("\n")[2], contenu.split("\n")[3], contenu.split("\n")[4], contenu.split("\n")[5], int(contenu.split("\n")[6]);

def main():
	old_timestamp = time.time();
	ck, cs, atk, ats, link, pseudo, wait = get_args();
	while True:
		api = init_tweet(ck, cs, atk, ats);
		entries = get_new_entries(link, old_timestamp);
		for item in entries:
			send_tweet(api,make_tweet(pseudo, item));
			if timestampisation(item.updated) > old_timestamp:
				old_timestamp = timestampisation(item.updated);
			time.sleep(2);
		print time.strftime("%d/%m/%y %H:%M:%S") + " : " + "Nothing more found, I'll take a litle break ;-)";
		time.sleep(wait);


main();
