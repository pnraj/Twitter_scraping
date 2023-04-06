# use pip show for checking the lib present in your machine
# libraries and modules for import

from datetime import date
import pandas as pd
import snscrape.modules.twitter as sntwitter
import streamlit as st
import pymongo

#page config setting layout = wide or centered
st.set_page_config(layout="wide", page_title='Get_Tweets') # layout = wide or centered

st.subheader("**:green[:man-raising-hand: Welcome to Twitter Scraping]**")

# Project intoduction
st.write(""" 
This website helps you to Scrape Tweets using a **keyword or hashtag** , date range, 
and total number of tweets needed. 
**snscrape** is used for scraping the tweets and the 
tweets get displayed in the GUI that built with **Streamlit** 
and which can be uploaded into **MongoDB** database and downloaded 
as a **CSV**,**JSON** file.For full details visit Project Repository""")

#Project Repository link
st.sidebar.header("Project Repository:[Twitter Scraping](https://github.com/pnraj/Twitter_scraping)")

# sidebar
st.sidebar.header("**:green[:point_down: Let's Begin Twitter Scraping]:point_down:**")

# Keyword/hastags, tweet count and date range(start and end)
Hashtag = st.sidebar.text_input("Enter the Hashtag or Keyword of Tweets : ")
No_of_tweets = st.sidebar.number_input("Number of Tweets needed : ", min_value= 1, max_value= 1000, step= 1)
st.sidebar.write(":green[Select the Date range]")
start_date = st.sidebar.date_input("Start Date (YYYY-MM-DD) : ")
end_date = st.sidebar.date_input("End Date (YYYY-MM-DD) : ")
Scraped_date = str(date.today())


# Creating a list to store tweets
Total_tweets = []

if Hashtag:
    # Using for loop, TwitterSearchScraper and enumerate function to scrape data and append tweets to list
    for a,tweet in enumerate(sntwitter.TwitterSearchScraper(f"{Hashtag} since:{start_date} until:{end_date}").get_items()):
        if a >= No_of_tweets:
            break
        Total_tweets.append([tweet.id,tweet.user.username,
                            tweet.lang,tweet.date,
                            tweet.url,tweet.replyCount,tweet.retweetCount,
                            tweet.likeCount,tweet.rawContent,
                            tweet.source
                           ])

# DataFrame from Total_tweets
def data_frame(t_data):
    return pd.DataFrame(t_data, columns= ['user_id','user_name','language','datetime',
                                          'url', 'reply_count','retweet_count', 'like_count', 
                                          'tweet_content','source'])

# DataFrame to JSON file
def convert_to_json(t_j):
    return t_j.to_json(orient='index')

# DataFrame to CSV file
def convert_to_csv(t_c):
    return t_c.to_csv().encode('utf-8')


# Creating objects for dataframe and file conversion
df = data_frame(Total_tweets)
csv = convert_to_csv(df)
json = convert_to_json(df)

# Using MongoDB Atlas as a new database to store date(scraped tweets) in collections(scraped_tweets)
client = pymongo.MongoClient("mongodb+srv://pnrajk:Nataraj1996@cluster0.rlu7bvd.mongodb.net/?retryWrites=true&w=majority")
db = client.twitterscraping
col = db.scraped_tweets
scr_data = {"Scraped_word" : Hashtag,
            "Scraped_date" : Scraped_date,
            "Scraped_tweets" : df.to_dict('records')
           }

if df.empty:
    st.subheader(":point_left:.Scraped tweets will visible after entering hashtag or keywords")

else:
    st.write("**:green[Choose any options from below]**")
    # Automatically load the DataFrame in Tabular Format
    st.success(f"**:green[{Hashtag} tweets]:thumbsup:**")
    st.write(df)
    
# Placing buttons horizontally
    b2 , b3, b4 = st.columns([43,40,30]) #it's distance is found by trial and error method
    
    # BUTTON  - To upload the data to mongoDB database
    if b2.button("Upload to MongoDB"):
            try:
                col.delete_many({})
                col.insert_one(scr_data)
                b2.success('Upload to MongoDB Successfully:thumbsup:')
            except:
                b2.error('Please try again after Submiting the Hashtag or keyword') 

    # BUTTON - To download data as CSV
    if b3.download_button(label= "Download CSV",
                            data= csv,
                            file_name= f'{Hashtag}_tweets.csv',
                            mime= 'text/csv'
                            ):
                b3.success('CSV Downloaded Successfully:thumbsup:')


    # BUTTON - To download data as JSON
    if b4.download_button(label= "Download JSON",
                        data= json,
                        file_name= f'{Hashtag}_tweets.json',
                        mime= 'text/csv'
                        ):
            b4.success('JSON Downloaded Successfully:thumbsup:')

        
if __name__ == "__main__":
    main()
