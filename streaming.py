from tweepy import Stream
from tweepy.streaming import StreamListener

from settings import auth


class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('mytweets.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#python'])


"""
We have introduced tweepy as a tool to access Twitter data in a fairly easy way with Python.
There are different types of data we can collect, with the obvious focus on the “tweet” object.
Once we have collected some data, the possibilities in terms of analytics applications are endless.
In the next episodes, we’ll discuss some options.
"""

"""
A project that collects twitter data using twitter api. Then data is preprocessed, analysed and sentimentally analysed; results are then visualized in charts and interactive maps.
Also sentiment analysis is done
Part 3: Term Frequencies
Part 4: Rugby and Term Co-Occurrences
Part 5: Data Visualisation Basics
Part 6: Sentiment Analysis Basics
Part 7: Geolocation and Interactive Maps
"""