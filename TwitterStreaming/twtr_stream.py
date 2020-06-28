from tweepy import Stream, StreamListener
import json
from TwitterStreaming import TwitterAuthenticator


# # # # TWITTER STREAMER # # # #
class TwitterStreamer:
    """
    Class for streaming and processing live tweets_by_country.
    """

    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list=None, follow=None):
        # This handles Twitter authetification and the connection to Twitter Streaming TwitterStreaming
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()  # does the authentication job
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture Data by the keywords:
        stream.filter(track=hash_tag_list, follow=follow)  # locations=location


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets_by_country to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    # def on_data(self, Data):
    #     try:
    #         print(Data)
    #         with open(self.fetched_tweets_filename, 'a') as tf:
    #             tf.write(Data)
    #         return True
    #     except BaseException as e:
    #         print("Error on_data %s" % str(e))
    #     return True
    def on_data(self, data):
        all_data = json.loads(data)
        print(all_data)
        # Open json text file to save the tweets_by_country
        with open(self.fetched_tweets_filename, 'a') as tf:
            # Write a new line
            tf.write('\n')
            # Write the json Data directly to the file
            json.dump(all_data, tf)
            # Alternatively: tf.write(json.dumps(all_data))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)
