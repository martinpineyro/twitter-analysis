from twython import Twython
import django
import csv
import time
import os
import keras

APP_KEY = ''
APP_SECRET = ''

twitter = Twython(APP_KEY, APP_SECRET)

auth = twitter.get_authentication_tokens()

OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']



with open('followers.csv', 'w', newline='') as f:
	f.write("id, name, screen_name, location, description, verified, followers_count, friends_count, favourites_count, statuses_count ,created_at\n")
f.close()

next_cursor = -1

while True:

	try:
		followers_list = twitter.get_followers_list(screen_name='', include_user_entities= 'true', cursor=str(next_cursor))
		
	except TwythonError as e:
		print(e)

	with open('followers.csv', 'a', newline='') as f:
		for user in followers_list['users']:
			user_id = user['id']
			user_name = str(' '.join(keras.preprocessing.text.text_to_word_sequence(user['name'], filters='\x0c0123456789!"#$%&()*+,-./:;<=>¿?@[\\]^_`{|}~\t\n', lower=True, split=' ')))
			user_screen_name = str(' '.join(keras.preprocessing.text.text_to_word_sequence(user['screen_name'], filters='\x0c0123456789!"#$%&()*+,-./:;<=>¿?@[\\]^_`{|}~\t\n', lower=True, split=' ')))
			user_location = str(' '.join(keras.preprocessing.text.text_to_word_sequence(user['location'], filters='\x0c0123456789!"#$%&()*+,-./:;<=>¿?@[\\]^_`{|}~\t\n', lower=True, split=' ')))
			user_description = str(' '.join(keras.preprocessing.text.text_to_word_sequence(user['description'], filters='\x0c0123456789!"#$%&()*+,-./:;<=>¿?@[\\]^_`{|}~\t\n', lower=True, split=' ')))
			user_verified = user['verified']
			user_followers_count = user['followers_count']
			user_friends_count = user['friends_count']
			user_favourites_count = user['favourites_count']
			user_statuses_count = user['statuses_count']
			user_created_at = user['created_at']

			#print(user['description'])

			f.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n"%(
				user_id,
				user_name,
				user_screen_name,
				user_location,
				user_description,
				user_verified,
				user_followers_count,
				user_friends_count,
				user_favourites_count,
				user_statuses_count,
				user_created_at
			    )
			)
	f.close()



	next_cursor = followers_list['next_cursor']	
	print(next_cursor)

	if next_cursor == 0:
		break

	time.sleep(60)


print(followers_list['previous_cursor'])
print(followers_list['next_cursor'])





