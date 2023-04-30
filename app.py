import streamlit as st
import matplotlib.pyplot as plt
import helper
import seaborn as sns
import preprocessor

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)


    # Fetch unique users OPEN

    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if(st.sidebar.button("Show Analysis")):
        st.title('Top Statistics')
        num_messages, words, num_media_messages, num_links, num_mem, unknown_members= helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(words)

        with col3:
            st.header('Media Shared')
            st.title(num_media_messages)

        with col4:
            st.header('Links Shared')
            st.title(num_links)

        with col5:
            st.header('Total Members')
            st.title(num_mem)

    # Fetch unique users CLOSED
        st.title('Chats in Tabular Data.')
        st.dataframe(df)

    #monthly-timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax =plt.subplots()
        ax.plot(timeline['time'],timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        plt.ylabel('Messages')
        st.pyplot(fig)

    #activity map
        st.title('Activity Map')
        col1,col2=st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busy_day=helper.week_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            plt.ylabel('Messages')
            plt.xlabel('Days')
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index,busy_day.values, color='#AD1457')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month=helper.month_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            plt.ylabel('Messages')
            plt.xlabel('Months')
            ax.bar(busy_month.index,busy_month.values, color='#746A80')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        act_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax=plt.subplots()
        ax=sns.heatmap(act_heatmap)

        plt.figure(figsize=(3, 3))
        st.pyplot(fig)
    #daily_timeline
        #st.title('Daily Timeline')
        #daily_timeline = helper.daily_timeline(selected_user, df)
        #fig, ax = plt.subplots()
        #ax.plot(daily_timeline['only_date'], timeline['message'], color='#AD1457')
        #plt.xticks(rotation='vertical')
        #st.pyplot(fig)

    #finding the busiest users in the group( Group Level) OPEN
        if selected_user == "Overall":
            st.title('Most Active Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax=plt.subplots()
            col1,col2=st.columns(2)

            with col1:
               ax.bar(x.index, x.values)
               plt.ylabel('Messages')
               plt.xlabel('Users')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


    #most common user
            st.title('Most Common Words')
            most_common_df = helper.most_common_words(selected_user,df)
            fig,ax = plt.subplots()
            plt.xlabel('No. of times repeated')
            plt.ylabel('Messages')
            ax.barh(most_common_df[0],most_common_df[1], color='#018571')

            st.pyplot(fig)



