import json
# with open('tweets.json', 'r') as f:
#     line = f.readline()  # read only the first tweet/line
#     tweet = json.loads(line)  # load it as Python dict
#     print(json.dumps(tweet, indent=4))  # pretty-print
import operator

import pandas

from settings import filter_value

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

# from nltk.tokenize import word_tokenize

# tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
# print(word_tokenize(tweet))
# ['RT', '@', 'marcobonzanini', ':', 'just', 'an', 'example', '!', ':', 'D', 'http', ':', '//example.com', '#', 'NLP']

import re
from nltk import bigrams
from nltk.corpus import stopwords
from collections import Counter, defaultdict
import string

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


punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT', '…', '’', '“']

count_hash = Counter()
count_terms_only = Counter()
count_bigrams = Counter()
com = defaultdict(lambda: defaultdict(int))
dates_of_tweets = []
dates_king = []
dates_fbi = []

with open('tweets.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_no_stop = [term for term in preprocess(tweet['text']) if term not in stop]

        terms_bigram = list(bigrams(terms_no_stop))
        # Count hashtags only
        terms_hash = [term for term in terms_no_stop
                      if term.startswith('#')]

        if filter_value in terms_hash:
            dates_of_tweets.append(tweet['created_at'])

        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in terms_no_stop
                      if term not in stop and
                      not term.startswith(('#', '@'))]

        if 'King' in terms_only:
            dates_king.append(tweet['created_at'])
        if 'FBI' in terms_only:
            dates_fbi.append(tweet['created_at'])

        for i in range(len(terms_only) - 1):
            for j in range(i + 1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])
                if w1 != w2:
                    com[w1][w2] += 1

        # Update the counter
        count_hash.update(terms_hash)
        count_terms_only.update(terms_only)
        count_bigrams.update(terms_bigram)
    # Print the first 5 most frequent words

    print('count_hash', count_hash.most_common(10))
    print('count_terms_only', count_terms_only.most_common(10))
    print('count_bigrams', count_bigrams.most_common(10))

    com_max = []
    # For each term, look for the most common co-occurrent terms
    for t1 in com:
        t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
        for t2, t2_count in t1_max_terms:
            com_max.append(((t1, t2), t2_count))
    # Get the most frequent co-occurrences
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    print(terms_max[:5])

import vincent

word_freq = count_terms_only.most_common(20)
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('term_freq.json')


# bar.to_json('term_freq.json', html_out=True, html_path='chart.html')

def build_per_minute(dates):
    # a list of "1" to count the hashtags
    ones = [1] * len(dates)
    # the index of the series
    idx = pandas.DatetimeIndex(dates)
    # the actual series (at series of 1s for the moment)
    data = pandas.Series(ones, index=idx)

    # Resampling / bucketing
    per_minute = data.resample('1Min').sum().fillna(0)

    return per_minute


per_minute = build_per_minute(dates_of_tweets)
time_chart = vincent.Line(per_minute)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('time_chart.json')

per_minute_king = build_per_minute(dates_king)
per_minute_fbi = build_per_minute(dates_fbi)
# all the data together
match_data = dict(King=per_minute_king, FBI=per_minute_fbi)
# we need a DataFrame, to accommodate multiple series
all = pandas.DataFrame(data=match_data,
                       index=per_minute_king.index)
# Resampling as above
all = all.resample('1Min').sum().fillna(0)

print('all')
print(all)
# and now the plotting
time_chart = vincent.Line(all[['King', 'FBI']])
time_chart.axis_titles(x='Time', y='Freq')
time_chart.legend(title='All')
time_chart.to_json('time_chart.json')
