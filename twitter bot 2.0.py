import tweepy
import time
import elizabot
CK=""
CS=""
AT=""
ATS=""
# Authenticate to Twitter
auth = tweepy.OAuthHandler(CK,CS)
auth.set_access_token(AT,ATS)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
replied_tweets_id=[]
print()
while(True):
    flag=0
    print('\n-----------------------checking tweets every 10 seconds------------------------\n')
    tweets = api.mentions_timeline()
    id_mentioned=[]
    if(len(tweets) != 0):
        for mentions in tweepy.Cursor(api.mentions_timeline).items():
        # process mentions here
            id_mentioned.append(mentions.id)
            
        #creating an empty list and appending all the text of tweets that the user was mentioned
        messages=[]
        for mentions in tweepy.Cursor(api.mentions_timeline).items():
            # process mentions here
            messages.append(mentions.text)

        #removing the username from all the text messages and sending it to eliza-bot to predict the response
        i=0
        for message in messages:
            if(id_mentioned[i] not in replied_tweets_id):
                reply=(elizabot.analyze(message.split(' ',1)[1]))
                api.update_status(status = reply , in_reply_to_status_id = id_mentioned[i] , auto_populate_reply_metadata=True)
                replied_tweets_id.append(id_mentioned[i])
                i=i+1
                print('\nThe tweet "',message,'" was replied with: "',reply,'"\n')
                flag=1
    if(flag==0):
          print('\n--------Already replied to all tweets/No mentions found,checking again----------\n')
    time.sleep(10)
            
