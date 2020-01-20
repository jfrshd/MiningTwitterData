from tweepy import Stream
from tweepy.streaming import StreamListener

from settings import auth, results_file, filter_value


class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open(results_file, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
while True:
    try:
        twitter_stream.filter(track=[filter_value])
    except Exception as e:
        print(e)
