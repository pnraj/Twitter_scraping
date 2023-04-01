
# Twitter Scraping 
This project aims to scrape Twitter data using the snscrape library, store it in **MongoDB**, and display the scraped data in a GUI built with **Streamlit**. The user can enter a **keyword or hashtag** to search, select a date range, and limit the number of tweets to scrape. The scraped data is displayed in the GUI and can be uploaded to the database, downloaded as a **CSV** or **JSON** file.

### Requirments for this project
- __[Python 3](https://docs.python.org/)__
- __[Snscrape](https://github.com/JustAnotherArchivist/snscrape)__
- __[Pymongo](https://pymongo.readthedocs.io/)__
- __[Pandas](https://pandas.pydata.org/docs/)__
- __[MongoDB Atlas](https://www.mongodb.com/docs/)__
- __[Streamlit](https://docs.streamlit.io/)__
- __[Datetime](https://docs.python.org/3/library/datetime.html)__

### Demo
A demo video of the working model is available on LinkedIn.
<p align="center">
  <a href="https://www.youtube.com/watch?v=StTqXEQ2l-Y">
    <img src="./tweets.png" width="640" height="360">
  </a>
  <br>
  <em>Click to watch the video</em>
</p>
https://img.youtube.com/vi/<insert-youtube-video-id-here>/0.jpg image of youtube videos

## Workflow

+ Step 0 `pip install snscrape pandas streamlit datetime pymongo`
+ Step 1 `Importing needed libraries`
``` py
from datetime import date
import pandas as pd
import snscrape.modules.twitter as sntwitter
import streamlit as st
import pymongo
```
+ Step 2 `Getting input from user on streamlit sidebar`

``` py
# Keyword/hastags, tweet count and date range(start and end)
Hashtag = st.sidebar.text_input("Enter the Hashtag or Keyword of Tweets : ")
No_of_tweets = st.sidebar.number_input("Number of Tweets needed : ", min_value= 1, max_value= 1000, step= 1)
st.sidebar.write(":green[Select the Date range]")
start_date = st.sidebar.date_input("Start Date (YYYY-MM-DD) : ")
end_date = st.sidebar.date_input("End Date (YYYY-MM-DD) : ")
Scraped_date = str(date.today())
```
+ Step 3 `Using snscrape and pandas,Tweets get scraped,converted into Dataframe and displayed in tabular format`
```py
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
```
+ Step 4 `Pymongo is used to connect to Mongodb Atlas` 
  + `Note: Change the API into your Mongodb atlas API, to avoid access restriction error`
``` py
# Using MongoDB Atlas as a new database to store date(scraped tweets) in collections(scraped_tweets)
client = pymongo.MongoClient("mongodb+srv://pnrajk1:Nataraj19961@cluster0.rlu7bvd.mongodb.net/?retryWrites=true&w=majority")
db = client.twitterscraping
col = db.scraped_tweets
scr_data = {"Scraped_word" : Hashtag,
            "Scraped_date" : Scraped_date,
            "Scraped_tweets" : df.to_dict('records')
           }
```
+ Step 5 `Streamlit is used to create GUI Buttons for Uploading and Downloading scraped tweets`
``` py
if df.empty:
    st.subheader(":point_left:.Scraped tweets will visible after entering hashtag or keywords")

else:
    # Automatically load the DataFrame in Tabular Format
    st.success(f"**:green[{Hashtag} tweets]:thumbsup:**")
    st.write(df)
    st.write("**:green[Choose Any options from below]**")
    
    # Button in horizontal order
    b2 , b3, b4 = st.columns([43,40,30]) 
    # GUI-Button2  - To upload the data to mongoDB database
    if b2.button("Upload to MongoDB"):
            try:
                col.delete_many({})
                col.insert_one(scr_data)
                b2.success('Upload to MongoDB Successfully:thumbsup:')
            except:
                b2.error('Please try again after Submiting the Hashtag or keyword') 

    # GUI-Button3 - To download data as CSV
    if b3.download_button(label= "Download CSV",
                            data= csv,
                            file_name= f'{Hashtag}_tweets.csv',
                            mime= 'text/csv'
                            ):
                b3.success('CSV Downloaded Successfully:thumbsup:')


    # GUI-Button4 - To download data as JSON
    if b4.download_button(label= "Download JSON",
                        data= json,
                        file_name= f'{Hashtag}_tweets.json',
                        mime= 'text/csv'
                        ):
            b4.success('JSON Downloaded Successfully:thumbsup:')
```
### To run the app, Navigate to the folder which app is present using CLI and run the command
``` py
streamlit run tweets.py
```
### Future Improvements
- Expand the project to scrape data from other social media platforms
- Add authentication to the GUI to ensure data privacy
- List of available Hashtags present in database

###### The project code follows the PEP 8 coding standards with detailed information on the project's workflow and execution.




