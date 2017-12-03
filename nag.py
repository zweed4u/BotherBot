#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime, random, tweepy, time
poll = 1800 # 1/2 hour
target = "" # the user you intend to nag
picture = "" # an image's filename that exists in the same directory as this script

#https://apps.twitter.com/app
consumerKey = ""
consumerSecret = ""
accessToken = ""
accessTokenSecret = ""

class Twitter:
	'''Twitter integration'''
	def __init__(self, apiKey, apiSecret, token, tokenSecret):
		self.apiKey = apiKey
		self.apiSecret = apiSecret
		self.token = token
		self.tokenSecret = tokenSecret

	def authenticate(self):
		global api
		auth = tweepy.auth.OAuthHandler(self.apiKey, self.apiSecret)
		auth.set_access_token(self.token, self.tokenSecret)
		api = tweepy.API(auth)

	def tweet(self, message):
		api.update_status(status=message)

	def tweet_media(self, file, message):
		api.update_with_media(file, status=message)

	def batch_delete(self):
		print "Deleting all tweets associated with account..."
		for status in tweepy.Cursor(api.user_timeline).items():
			api.destroy_status(status.id)
		print "Done with deletions"

def UTCtoEST():
	current = datetime.datetime.now()
	return str(current) + ' EST'

if __name__ == '__main__':
	my_twitter = Twitter(consumerKey, consumerSecret, accessToken, accessTokenSecret) #twitter auth instance
	my_twitter.authenticate()
	my_twitter.batch_delete()


	epoch_date = datetime.datetime(1970, 1, 1) # just delta time tweet useful for anniversary
	previous_tweet = ""
	selections = [
		# a pool
		# of tweets
		# that will
		# be randomly
		# chosen from
	]
	while 1:
		# Set delta time tweet with proper time
		today = datetime.datetime.now()
		epoch_date_tweet = "Time since epoch: {} days, {} seconds, {} microseconds".format((today-epoch_date).days, (today-epoch_date).seconds, (today-epoch_date).microseconds)
		selections.append(epoch_date_tweet)

		# Pick a tweet
		chosen_message = selections[random.randint(0,len(selections)-1)]

		# Remove what was picked so it cant be tweeted again
		selections.remove(chosen_message)

		# Remove the epoch tweet so that we can update the time for when its tweeted
		if epoch_date_tweet in selections:
			selections.remove(epoch_date_tweet)

		# We have cycled through the whole list! Reload 
		# TODO: delete all previous tweets too
		if len(selections) == 0:
			my_twitter.batch_delete()
			selections = [
				# a pool
				# of tweets
				# that will
				# be randomly
				# chosen from
			]
		if chosen_message == "dummy text": # this string is a trigger to tweet media with this caption
			try:
				my_twitter.tweet_media(picture, "@{} {}".format(target, chosen_message))

				# Log tweet for my view
				print "{} : {}".format(UTCtoEST(), chosen_message)
			except:
				continue

		else:
			# Send tweet off
			try:
				my_twitter.tweet("@{} {}".format(target, chosen_message))

				# Log tweet for my view
				print "{} : {}".format(UTCtoEST(), chosen_message)
			except:
				continue

		# Sleep until time to tweet again
		time.sleep(poll)

		# Used for tracking previous tweet
		previous_tweet = chosen_message
