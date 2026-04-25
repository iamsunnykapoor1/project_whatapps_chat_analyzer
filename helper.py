from fontTools.misc.cython import returns
from urlextract import URLExtract
from wordcloud import WordCloud

import pandas as pd
from collections import Counter

import string

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('hinglish'))


def fetch_stats(selected_user,df):

    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    # fetch the number of messages
    num_messages = df.shape[0]
    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    #fetch the number of media messages
    num_media_messages =df[df['message'] == "<Media omitted>\n"].shape[0]

    #fetch the number of link share
    extractor = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))


    return num_messages, len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns = {'user' : 'name' ,'count' : 'percentage'})
    return x ,df


def create_wordcloud(selected_user ,df) :

    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and string.punctuation:
                words.append(word)

    wc  = WordCloud(width=500 ,height=500 ,min_font_size=10,background_color='white')
    df_wc = wc.generate(" ".join(words))
    return df_wc


def most_common_words(selected_user ,df):
    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and string.punctuation:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

