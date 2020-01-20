import json

with open('mytweets.json', 'r') as f:
    line = f.readline()  # read only the first tweet/line
    tweet = json.loads(line)  # load it as Python dict
    print(json.dumps(tweet, indent=4))  # pretty-print

"""
text: the text of the tweet itself
created_at: the date of creation
favorite_count, retweet_count: the number of favourites and retweets
favorited, retweeted: boolean stating whether the authenticated user (you) have favourited or retweeted this tweet
lang: acronym for the language (e.g. “en” for english)
id: the tweet identifier
place, coordinates, geo: geo-location information if available
user: the author’s full profile
entities: list of entities like URLs, @-mentions, hashtags and symbols
in_reply_to_user_id: user identifier if the tweet is a reply to a specific user
in_reply_to_status_id: status identifier id the tweet is a reply to a specific status
"""
from nltk.tokenize import word_tokenize

tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
print(word_tokenize(tweet))
# ['RT', '@', 'marcobonzanini', ':', 'just', 'an', 'example', '!', ':', 'D', 'http', ':', '//example.com', '#', 'NLP']

import re

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


# tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
# print(preprocess(tweet))
# ['RT', '@marcobonzanini', ':', 'just', 'an', 'example', '!', ':D', 'http://example.com', '#NLP']

with open('mytweets.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        tokens = preprocess(tweet['text'])
        do_something_else(tokens)


"""
In this file we have analysed the overall structure of a tweet, 
and we have discussed how to pre-process the text before we can get into some more interesting analysis.
In particular, we have seen how tokenisation, despite being a well-understood problem, can get tricky with Twitter data.
The proposed solution is far from perfect but it’s a good starting point, and fairly easy to extend.
"""