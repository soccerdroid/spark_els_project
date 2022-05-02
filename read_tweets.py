
import pyspark

# import necessary packages
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import desc
from pyspark.mllib.linalg import Vectors


from textblob import TextBlob

def get_sentiment(text):
    tb = TextBlob(text)
    return round(tb.sentiment.polarity, 2)

def get_vector(line):
    if len(line.strip().split('|')) == 3 and line.strip().split('|')[1].isnumeric() and line.strip().split('|')[2].isnumeric():
        text, followers_count, friends_count = line.strip().split('|')
        followers_count = int(followers_count)
        friends_count = int(friends_count)
        sent = get_sentiment(text)
        return [sent, followers_count, friends_count]
    return None

sc = SparkContext()
# we initiate the StreamingContext with 10 second batch interval. #next we initiate our sqlcontext
ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)


# initiate streaming text from a TCP (socket) source:
socket_stream = ssc.socketTextStream("127.0.0.1", 5555)
# lines of tweets with socket_stream window of size 60, or 60 #seconds windows of time
lines = socket_stream.window(60)

#sent = lines.flatMap(lambda line: line.split(" "))
#sent = lines.map(lambda line: get_sentiment(str(line).split('|')[0]))

#sent.pprint()


#trainingData = lines.map(lambda line: Vectors.dense(get_vector(line.strip())))
#trainingData = lines.map(lambda line: get_vector(line.strip()))
trainingData = lines.map(lambda line: line)
trainingData.pprint()


#lines.flatMap(lambda line: line.split(" ")).pprint()
#counts = lines.flatMap(lambda line: line.split(" "))\
#              .map(lambda word: (word, 1))\
#              .reduceByKey(lambda a, b: a+b)
#counts.pprint()
ssc.start()
ssc.awaitTermination()
