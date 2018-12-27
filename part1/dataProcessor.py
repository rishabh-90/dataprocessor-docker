import pandas as pd
from dateutil import parser
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import feedparser
import time
import psycopg2
import sys
from sqlalchemy import create_engine, MetaData, Table, Column, TEXT, VARCHAR, DateTime
nltk.download('punkt')
nltk.download('stopwords')

#Common Variables for the Script
stop_words = stopwords.words('english')
engine = create_engine('postgresql://postgres:example@db:5432/postgres') #Connection to the Postgres Working in different container
repeat_time_seconds = int(float(sys.argv[1])*60*60) #Time interval for the checking the feed after Nth hour

def push_postgres_table(df, table, engine):
    '''
        This Function will push data in the Postgres it takes 3 variables.
        df = Pandas DataFrame, Table = Table name in String, Engine = Sqlalchemy create_engine
    '''
    try:
        engineCon = engine.connect()
        df = df.to_sql(table, engineCon, index=False, if_exists='append')
    finally:
        engineCon.close()
    return df

def get_max_date_postgre():
    '''
        This Function will max date from the Postgres table.
        df = Pandas DataFrame, Table = Table name in String, Engine = Sqlalchemy create_engine
        It return Date or Emty string if nothing found
    '''
    query = 'Select max("Pipeline_Update") from "Data_Pipeline"'
    try: 
        engineCon = engine.connect()
        df = pd.read_sql_query(query, engineCon)
    finally:
        engineCon.close()
    return df['max'].iloc[0]

def push_feed_database(engine,rss_feed,papers):
    '''
        This Function will push feeds to database.
    '''
    for paper in rss_feed.entries:
        if 'CROSS LISTED' in paper.title or 'UPDATED' in paper.title: #Filter New Submissions from the feed leaving crosslisted and replc
            pass
        else:
            title = re.sub(r'\(arXiv:.+\)','',paper.title).rstrip()
            title = re.sub('[^A-Za-z0-9]+', ' ', title)
            description = re.sub('<[^<]+?>', '', paper.summary) #removes HTML tags from the Description of the paper
            tokens = word_tokenize(description) #create Word tokens for removal of stop words, punctuations and making every word to lower
            words = [word.lower() for word in tokens if word.isalpha()]
            words = [w for w in words if not w in stop_words]
            description = " ".join(words)
            papers.append((title,paper.link,description,parser.parse(rss_feed.feed.updated).replace(tzinfo=None))) #creating tuples which will we passed to Pandas Dataframe
    new_df = pd.DataFrame(papers,columns=['Title','Link','Description','Pipeline_Update']) 
    print(new_df.head())
    push_postgres_table(new_df, 'Data_Pipeline', engine)
    print('Data has been Pushed')


if not engine.dialect.has_table(engine, 'Data_Pipeline'):  # If table don't exist, Create.
    metadata = MetaData(engine)
    # Create a table with the appropriate Columns
    meta = MetaData(engine)
    t1 = Table('Data_Pipeline', meta,Column('Title', VARCHAR(500)),Column('Link',VARCHAR(50)),Column('Description',TEXT),Column('Pipeline_Update',DateTime))
    # Implement the creation
    t1.create()

while True:
    print('Started')
    papers = [] #intialize empty list to hold required information from the feed
    rss_feed = feedparser.parse('http://export.arxiv.org/rss/cs') #Request Feed using feedparser
    max_date = get_max_date_postgre() #check for the Date from the Pipeline_Update for maximum date to make desicion logic to process feed or not.
    print(parser.parse(rss_feed.feed.updated))
    if len(rss_feed.entries) > 0: # If Feed Length is greater than 0 then only it is feasible to process data
        if max_date is None:
            push_feed_database(engine,rss_feed,papers)
        else:
            if parser.parse(rss_feed.feed.updated).replace(tzinfo=None) > max_date: #This will Update the records in Table when Feed is new
                print('Working')
                push_feed_database(engine,rss_feed,papers)
            elif parser.parse(rss_feed.feed.updated).replace(tzinfo=None) == max_date: # This Condition will work when the Date in the Database and Feed in the Feed is Similar
                print('Feed and Database is upto date')
            else: #This condition should run when Database is Empty
                push_feed_database(engine,rss_feed,papers)
    else:
        print("Nothing to Update")
    time.sleep(repeat_time_seconds)

