import tweepy
from tweepy.auth import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json

consumer_key    = ''
consumer_secret = ''
access_token    = ''
access_secret   = ''


from textblob import TextBlob

def get_sentiment(text):
    tb = TextBlob(text)
    return round(tb.sentiment.polarity, 2)

#class TweetsListener(Stream):
class TweetsListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket
    # we override the on_data() function in StreamListener
    def on_data(self, data):
        try:
            message = json.loads( data )
            text = message['text'].replace('|', '')
            followers_count = message['user']['followers_count']
            friends_count = message['user']['friends_count']
            socket_msg = text + '|' + str(followers_count) + '|' + str(friends_count)

            text, followers_count, friends_count = socket_msg.split('|')
            followers_count = int(followers_count)
            friends_count = int(friends_count)
            sent = get_sentiment(text)
            print(text)
            print(followers_count)
            print(friends_count)
            print(type(followers_count))
            print(type(friends_count))
            print(sent)
            print()
            self.client_socket.send( socket_msg.encode('utf-8') )

            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def if_error(self, status):
        print(status)
        return True

#    def on_error(self, status):
#        print(status)
#        return True
    
    
def send_tweets(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=['johnny depp', 'amber heard'], languages=['en']) #we are interested in this topic.


if __name__ == "__main__":
    new_skt = socket.socket()         # initiate a socket object
    host = "127.0.0.1"     # local machine address
    port = 5555                 # specific port for your service.
    new_skt.bind((host, port))        # Binding host and port

    print("Now listening on port: %s" % str(port))

    new_skt.listen()                 #  waiting for client connection.
    c, addr = new_skt.accept()        # Establish connection with client. it returns first a socket object,c, and the address bound to the socket

    print("Received request from: " + str(addr))

    # and after accepting the connection, we aill sent the tweets through the socket
    send_tweets(c)


