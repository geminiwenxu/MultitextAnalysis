from TwitterStreaming.twtr_stream import TwitterStreamer

if __name__ == '__main__':
    '''streaming live tweets_by_country with the keywords'''
    hash_tag_list = ['covid-19', 'coronavirus', 'socialdistance', 'socialdistancing', 'globalpandemic', 'stayathome','FightCOVID19']
    fetched_tweets_filename = "../Data/tweets_stream/live_stream_11.json"
    tweets_streamer = TwitterStreamer()
    tweets_streamer.stream_tweets(hash_tag_list=hash_tag_list,
                                  fetched_tweets_filename=fetched_tweets_filename)

    '''tweets_by_country stream from a specific user with keyword'''
    # hash_tag_list = ['covid-19', 'coronavirus', 'socialdistance', 'socialdistancing',
    #                  'globalpandemic', 'coronavuris',
    #                  'stayathome']
    # fetched_tweets_filename = 'tweets_by_country/nyt.json'
    # follow = ['807095']
    # user_tweets = TwitterStreamer()
    # user_tweets.stream_tweets(fetched_tweets_filename=fetched_tweets_filename,
    #                           hash_tag_list=hash_tag_list,
    #                           follow=follow)

    '''using TwitterStreaming class feature to extract Data from specific users'''
    # news = TwitterClient('2501296444')
    # for tweet in news.get_user_timeline_tweets(3200):
    #     print(tweet)
    #     tweet_df = TweetAnalyzer.filter_convert_pd(tweet)
    #     tweet_df.to_csv('tweets_by_country/denmark.csv', mode='a', header=False)

    '''Alternative'''
    # twitter_client = TwitterClient()
    # tweet_analyzer = TweetAnalyzer()
    # api = twitter_client.get_twitter_client_api()
    #
    # tweets_by_country = api.user_timeline(screen_name="nytimes", count=200, max_id=1263393231833960451) # 1264654931992227841
    # user_info = api.get_user(screen_name='nytimes')

    # print("all features we can extract from tweets_by_country: ", dir(tweets_by_country[0]))
    # print("retweet_count", tweets_by_country[0].retweet_count)
    # print("retweet", tweets_by_country[0].retweet)

    # to let pycharm built-in console displays all columns
    # desired_width = 3200
    # pd.set_option('display.width', desired_width)
    # pd.set_option('display.max_columns', 10)
    # pd.set_option('display.max_rows', 1000)
    #
    # df = tweet_analyzer.tweets_to_data_frame(tweets_by_country)
    # print("the first 10 elements from the Data frame df",df.head(3200))
