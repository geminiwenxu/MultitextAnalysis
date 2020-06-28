import time

from tweepy import API, Cursor, OAuthHandler, RateLimitError

from TwitterStreaming import twtr_config


# # # # TWITTER AUTHENTIFICATIOR # # # #
class TwitterAuthenticator:

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twtr_config.Consumer_key, twtr_config.Consumer_secret_key)
        auth.set_access_token(twtr_config.Access_token, twtr_config.Acess_token_secret)
        return auth


# # # # TWITTER CLIENT # # # #
class TwitterClient:
    def __init__(self, twitter_user=None):  # by default, if None, it goes into your own timeline
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    @staticmethod
    def limit_handled(cursor):
        while True:
            try:
                yield cursor.next()
            except RateLimitError:
                print('RateLimitError, sleeping...')
                time.sleep(15 * 60)
            except StopIteration:
                return

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in self.limit_handled(Cursor(self.twitter_client.user_timeline,
                                               id=self.twitter_user).items(num_tweets)):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
