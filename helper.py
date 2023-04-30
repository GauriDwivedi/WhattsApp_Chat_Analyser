import matplotlib.pyplot as plt
import pandas as pd
from urlextract import URLExtract
from collections import Counter
extract= URLExtract()


def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Fetch number of messages
    num_messages = df.shape[0]

    # Fetch number of words
    words = []
    for messages in df['message']:
        words.extend(messages.split())


    #Fetch number of media messages
    num_media_messages=df[df['message']=="<Media omitted>\n"].shape[0]

    # Fetch number of links in messages
    links = []
    for messages in df['message']:
        links.extend(extract.find_urls(messages))

    members=[]
    for mem in df['user']:
        if(mem!='group notification' and mem not in members):
            members.append(mem)

    unknown_members = []
    for unknown in df['user']:
        if (unknown != 'group notification' and unknown.isnumeric()):
            unknown_members.append(unknown)


    return num_messages, len(words), num_media_messages, len(links), len(members), len(unknown_members)

"""
    if selected_user == "Overall":

        # Fetch number of messages
        num_messages= df.shape[0]

        #Fetch number of words
        words=[]
        for messages in df['message']:
            words.extend(messages.split())
        return num_messages, len(words)
    else:
        new_df=df[df['user']== selected_user]
        num_messages = new_df.shape[0]
        words=[]
        for messages in new_df['message']:
            words.extend(messages.split())
        return num_messages, len(words)"""

def most_busy_users(df):
    x = df['user'].value_counts().head(10)

    df = round(((df['user'].value_counts()/df.shape[0])*100),2).reset_index().rename(columns={'index':'Name','user':'Percentage'})
    return x,df

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(21))
    return most_common_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    act_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return act_heatmap

