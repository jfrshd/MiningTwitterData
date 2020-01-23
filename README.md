<h1>Mining Twitter Data</h1>

Twitter is a popular social network where users can share short SMS-like messages called tweets. Users share thoughts, links and pictures on Twitter, journalists comment on live events, companies promote products and engage with customers. The list of different ways to use Twitter could be really long, and with 500 millions of tweets per day, there’s a lot of data to analyse and to play with.

<hr>

<h4><b>streaming.py:</b></h4>
We have introduced tweepy as a tool to access Twitter data in a fairly easy way with Python. There are different types of data we can collect, we focus on the “tweet” object. We have collected some data tracking `#MLKDay` hashtag, data is then saved into `tweets.json`.

<h4><b>main.py:</b></h4>

First, the overall structure of a tweet is analysed, The tweet is then tokenized using `nltk.tokenze()`, but we found conflicts with URLs, @-mentions, hashtags and symbols so we create our own regex expressions to be used instead.
Then the tokenization job is started on our collected tweets.

We then extracted interesting terms from a data set of tweets, by using simple term frequencies, stop-word removal and n-grams.

In this project, we did some text mining on Twitter, using some realistic data taken on Martin Luther King's Day `#MLKDay`. We have downloaded some data using the streaming API, pre-processed the data in JSON format and extracted some interesting terms and hashtags from the tweets. The project has also introduced the concept of term co-occurrence and built a co-occurrence matrix and used it to find some interesting insight.

Data is then visualized using `Vincent` which is a great tool that can easily bridge the gap between Python and a language like Javascript that offers a great tool like D3.js, one of the most important libraries for interactive visualisation. And then geodata of the tweets is visualized using `Leaflet` javascript library.   