#!env python
'''
Copyright 2014-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
'''
from __future__ import print_function
import sys, random, time, argparse
from boto import kinesis
import numpy as np

class Taxi_Location:
    num = 0
    max_lat = 40.89985962
    min_lat = 40.52729818
    max_lon = -73.70907059
    min_lon = -74.22954655
    mean_deglat_per_10m = 2.99437E-05
    mean_deglon_per_10m = 4.23496E-05

    def __init__(self):
        self.id = Taxi_Location.num
        Taxi_Location.num += 1
        self.latitude = np.random.normal(((Taxi_Location.min_lat+Taxi_Location.max_lat)/2),((Taxi_Location.max_lat-Taxi_Location.min_lat)/3))
        self.longitude = np.random.normal(((Taxi_Location.min_lon+Taxi_Location.max_lon)/2),((Taxi_Location.max_lon-Taxi_Location.min_lon)/3))

    def randomise(self):
        self.latitude += np.random.normal()*Taxi_Location.mean_deglat_per_10m
        if self.latitude < Taxi_Location.min_lat:
            self.latitude = Taxi_Location.min_lat
        elif self.latitude > Taxi_Location.max_lat:
            self.latitude = Taxi_Location.max_lat

        self.longitude += np.random.normal()*Taxi_Location.mean_deglon_per_10m
        if self.longitude < Taxi_Location.min_lon:
            self.longitude = Taxi_Location.min_lon
        elif self.longitude > Taxi_Location.max_lon:
            self.longitude = Taxi_Location.max_lon

    def get_latlon(self):
        return str(self.latitude)+','+str(self.longitude)

def get_stream_status(conn, stream_name):
    '''
    Query this provided connection object for the provided stream's status.

    :type conn: boto.kinesis.layer1.KinesisConnection
    :param conn: A connection to Amazon Kinesis

    :type stream_name: str
    :param stream_name: The name of a stream.

    :rtype: str
    :return: The stream's status
    '''
    r = conn.describe_stream(stream_name)
    description = r.get('StreamDescription')
    return description.get('StreamStatus')

def wait_for_stream(conn, stream_name):
    '''
    Wait for the provided stream to become active.

    :type conn: boto.kinesis.layer1.KinesisConnection
    :param conn: A connection to Amazon Kinesis

    :type stream_name: str
    :param stream_name: The name of a stream.
    '''
    SLEEP_TIME_SECONDS = 3
    status = get_stream_status(conn, stream_name)
    while status != 'ACTIVE':
        print('{stream_name} has status: {status}, sleeping for {secs} seconds'.format(
                stream_name = stream_name,
                status      = status,
                secs        = SLEEP_TIME_SECONDS))
        time.sleep(SLEEP_TIME_SECONDS) # sleep for 3 seconds
        status = get_stream_status(conn, stream_name)

def put_loc_in_stream(conn, stream_name, taxis):
    '''
    Put each word in the provided list of words into the stream.

    :type conn: boto.kinesis.layer1.KinesisConnection
    :param conn: A connection to Amazon Kinesis

    :type stream_name: str
    :param stream_name: The name of a stream.

    :type words: list
    :param words: A list of strings to put into the stream.
    '''
    for t in taxis:
        try:
            t.randomise()
            conn.put_record(stream_name, t.get_latlon(), str(t.id)) #data,partitionkey
            print("Put loc: " + t.get_latlon() + " into stream: " + stream_name+ " with partitionkey: " + str(t.id))
        except Exception as e:
            sys.stderr.write("Encountered an exception while trying to put a loc: "
                             + t.get_latlon() + " into stream: " + stream_name + " exception was: " + str(e))

def put_loc_in_stream_periodically(conn, stream_name, taxis, period_seconds):
    '''
    Puts words into a stream, then waits for the period to elapse then puts the words in again. There is no strict
    guarantee about how frequently we put each word into the stream, just that we will wait between iterations.

    :type conn: boto.kinesis.layer1.KinesisConnection
    :param conn: A connection to Amazon Kinesis

    :type stream_name: str
    :param stream_name: The name of a stream.

    :type words: list
    :param words: A list of strings to put into the stream.

    :type period_seconds: int
    :param period_seconds: How long to wait, in seconds, between iterations over the list of words.
    '''
    while True:
        put_loc_in_stream(conn, stream_name, taxis)
        print("Sleeping for {period_seconds} seconds".format(period_seconds=period_seconds))
        time.sleep(period_seconds)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('''
Puts words into a stream.

# Using the -w option multiple times
sample_wordputter.py -s STREAM_NAME -w WORD1 -w WORD2 -w WORD3 -p 3

# Passing input from STDIN
echo "WORD1\\nWORD2\\nWORD3" | sample_wordputter.py -s STREAM_NAME -p 3
''')
    parser.add_argument("-s", "--stream", dest="stream_name", required=True,
                      help="The stream you'd like to create.", metavar="STREAM_NAME",)
    parser.add_argument("-r", "--regionName", "--region", dest="region", default="us-west-1",
                      help="The region you'd like to make this stream in. Default is 'us-west-1'", metavar="REGION_NAME",)
    parser.add_argument("-p", "--period", dest="period", type=int, default=10,
                      help="If you'd like to repeatedly put words into the stream, this option provides the period for putting "
                            + "words into the stream in SECONDS. If no period is given then the words are put every 10s.",
                      metavar="SECONDS",)
    parser.add_argument("-n", "--numTaxi", dest="numTaxi", type=int, default=100,
                      help="The number of taxis to initialise",
                      metavar="TAXIS",)
    args = parser.parse_args()
    stream_name = args.stream_name

    '''
    Getting a connection to Amazon Kinesis will require that you have your credentials available to
    one of the standard credentials providers.
    '''
    print("Connecting to stream: {s} in {r}".format(s=stream_name, r=args.region))
    conn = kinesis.connect_to_region(region_name = args.region)
    try:
        status = get_stream_status(conn, stream_name)
        if 'DELETING' == status:
            print('The stream: {s} is being deleted, please rerun the script.'.format(s=stream_name))
            sys.exit(1)
        elif 'ACTIVE' != status:
            wait_for_stream(conn, stream_name)
    except:
        # We'll assume the stream didn't exist so we will try to create it with just one shard
        conn.create_stream(stream_name, 1)
        wait_for_stream(conn, stream_name)
    # Now the stream should exist, let's populate with Taxis
    taxis = []
    for i in range(args.numTaxi):
        taxis.append(Taxi_Location())
    put_loc_in_stream_periodically(conn, stream_name, taxis, args.period)
    # if len(args.words) == 0:
    #     print('No -w options provided. Waiting on input from STDIN')
    #     words = [l.strip() for l in sys.stdin.readlines() if l.strip() != '']
    # else:
    #     words = args.words
    # if args.period != None:
    #     put_words_in_stream_periodically(conn, stream_name, words, args.period)
    # else:
    #     put_words_in_stream(conn, stream_name, words)
