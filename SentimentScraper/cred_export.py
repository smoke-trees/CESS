import json

# create a dictionary to store your twitter credentials

twitter_cred = dict()

# Enter your own consumer_key, consumer_secret, access_key and access_secret
# Replacing the stars ("********")

twitter_cred['CONSUMER_KEY'] = 'ajks1S4glhFg6uwHQ9CEul3FV'
twitter_cred['CONSUMER_SECRET'] = 'EDGX7V8Kpxomg9X9Yb9nr00CjI2WSFpcw4TJpi5kichlvCr4WT'
twitter_cred['ACCESS_KEY'] = '2271791545-oZWJHPTbXZYEqy4A6jUC12R06Rjif9unzcrKMwj'
twitter_cred['ACCESS_SECRET'] = 'DmlXUWbXhnY6JUBDal6ZYfUYooGKxhbqrvO30fXpmVVoJ'

# Save the information to a json so that it can be reused in code without exposing
# the secret info to public

with open('twitter_credentials.json', 'w') as secret_info:
    json.dump(twitter_cred, secret_info, indent=4, sort_keys=True)
