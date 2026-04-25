import streamlit as st
from wordcloud import WordCloud

import preprocessor ,helper
import matplotlib.pyplot as plt

from helper import most_common_words


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    #st.text(data) to show the text data
    df = preprocessor.preprocess(data)
   # st.dataframe(df) # to show the data frame

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis") :# after clicking this analysis will start

        num_messages ,words ,num_media_messages, links = helper.fetch_stats(selected_user,df)

        st.title("Top statistics")

        col1 , col2 ,col3 ,col4 = st.columns(4)

        with col1 :
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total words", words)
        with col3:
            st.metric("Media share" ,num_media_messages)
        with col4:
            st.metric("links share",links)

        # timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        plt.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # finding the busiest user in the group(group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x ,new_df = helper.most_busy_users(df)
            fig , ax = plt.subplots()
            col1,col2 = st.columns(2)

            with col1 :
                ax.bar(x.index, x.values, color ='green')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2 :
                st.dataframe(new_df)

        # WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df )
        fig ,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

       # most common word
        st.title("Most common words")
        most_common_df = helper.most_common_words(selected_user, df)

        fig,ax =plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation ='vertical')

        st.pyplot(fig)



