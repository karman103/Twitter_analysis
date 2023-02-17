import tweepy
import credentials_tweepy
from pandas import DataFrame
# tweeting with vscode
api_key = credentials_tweepy.API_KEY
api_key_secret = credentials_tweepy.API_KEY_SECRET
bearer_token = credentials_tweepy.BEARER_TOKEN
access_token = credentials_tweepy.ACCESS_TOKEN
access_token_secret = credentials_tweepy.ACCESS_TOKEN_SECRET
auth =tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token ,access_token_secret)
api =tweepy.API(auth)
tweetmessage = 'Hello world from Python Tweepy'
#api.update_status(tweetmessage)


#tweets of elon musk
elon_userID = 'elonmusk'
elon_tweets = api.user_timeline(screen_name=elon_userID, 
                           count=10, 
                           include_rts = True,
                           exclude_replies = True,
                           tweet_mode = 'extended'
                           )

for elon_tweet in elon_tweets:
     print("ID: {}".format(elon_tweet.id))
     print(elon_tweet.created_at)
     print(elon_tweet.full_text)
     print("\n")

#tweets of man utd
userID = 'ManUtd'
tweets = api.user_timeline(screen_name=userID, 
                           count=200, 
                           include_rts = False,
                           exclude_replies = True,
                           tweet_mode = 'extended')

tweetCollector = []
tweetCollector.extend(tweets)
latestTweetId = tweets[-1].id

while True:
    tweets = api.user_timeline(screen_name=userID, 
                           count=200, 
                           include_rts = False,
                           exclude_replies = True,
                           tweet_mode = 'extended',
                           max_id = latestTweetId - 1)
    
    if len(tweets) == 0:
        print('Tweets = 0')
        break
        
    latestTweetId = tweets[-1].id
    tweetCollector.extend(tweets)
    print('Tweets downloaded so far: {}'.format(len(tweetCollector)))
# Saving all the tweets

tweetsHelper = [['Manchester United',
                tweet.id_str, 
                tweet.created_at, 
                tweet.favorite_count, 
                tweet.retweet_count, 
                tweet.full_text.encode("utf-8").decode("utf-8").replace('\n', ' ')] 
                for idx,tweet in enumerate(tweetCollector)]
                
df = DataFrame(tweetsHelper,columns=["club","id","createdAt","favorites","retweets",'likes',"text"])
df.to_csv('Tweets_%s.csv' % userID,index=False)
