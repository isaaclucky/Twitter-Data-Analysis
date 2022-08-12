import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from migrate_data import db_execute_fetch
import pickle

# model codes

def compute_sentiment(n,sentence):
     
    models = load_all(model=True)
    vectorizers = load_all(model = False)
    data=sentence
    if n>1:
        data=vectorizers[n%2].transform(sentence)
    return predict(vectoriser=vectorizers[n],model = models[n][4][1],text=data)
    

def load_single(name):
    file = open(name, 'rb')
    data = pickle.load(file)
    file.close()
    return data


def load_all(model=True):
    add = ''
    if not model:
        add = '_vectorizer'
    bigram = load_single('bigram'+add+'.pkl')
    trigram = load_single('trigram'+add+'.pkl')
    

    return [bigram, trigram]


def predict(vectoriser, model, text):
    # Predict the sentiment
    
    textdata = vectoriser.transform([text])
    
    sentiment = model.predict(textdata)
    return sentiment[0]



st.set_page_config(
    page_title="Twitter Data Analysis for China-USA topic", layout="wide")


def loadData():
    query = "select * from TweetInformation"
    df = db_execute_fetch(query, dbName="Twitter", rdf=True)
    return df


def selectHashTag():
    df = loadData()
    hashTags = st.multiselect(
        "choose combaniation of hashtags", list(df['hashtags'].unique()))
    if hashTags:
        df = df[np.isin(df, hashTags).any(axis=1)]
        st.write(df)


def selectLocAndAuth():
    df = loadData()
    location = st.multiselect(
        "choose Location of tweets", list(df['place'].unique()))
    lang = st.multiselect("choose Language of tweets",
                          list(df['lang'].unique()))

    if location and not lang:
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    elif lang and not location:
        df = df[np.isin(df, lang).any(axis=1)]
        st.write(df)
    elif lang and location:
        location.extend(lang)
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    else:
        st.write(df)


def barChart(data, title, X, Y):
    title = title.title()
    st.title(f'{title} Chart')
    msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                order='ascending')), y=f"{Y}:Q"))
    st.altair_chart(msgChart, use_container_width=True)


def wordCloud():
    df = loadData()
    cleanText = ''
    for text in df['original_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=650, height=450, background_color='white',
                   min_font_size=5).generate(cleanText)
    st.title("Tweet Text Word Cloud")
    st.image(wc.to_array())


def stBarChart():
    df = loadData()
    dfCount = pd.DataFrame({'Tweet_count': df.groupby(['original_author'])[
                           'original_text'].count()}).reset_index()
    dfCount["original_author"] = dfCount["original_author"].astype(str)
    dfCount = dfCount.sort_values("Tweet_count", ascending=False)

    num = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {num} Ranking By Number of tweets"
    barChart(dfCount.head(num), title, "original_author", "Tweet_count")


# def computeSentiment():
#     df = loadData()


def langPie():
    df = loadData()
    dfLangCount = pd.DataFrame({'Tweet_count': df.groupby(
        ['lang'])['original_text'].count()}).reset_index()
    dfLangCount["lang"] = dfLangCount["lang"].astype(str)
    dfLangCount = dfLangCount.sort_values("Tweet_count", ascending=False)
    dfLangCount.loc[dfLangCount['Tweet_count']
                    < 10, 'lang'] = 'Other languages'
    st.title(" Tweets Language pie chart")
    fig = px.pie(dfLangCount, values='Tweet_count',
                 names='lang', width=500, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    colB1, colB2 = st.columns([2.5, 1])

    with colB1:
        st.plotly_chart(fig)
    with colB2:
        st.write(dfLangCount)


fig_col1, fig_col2 = st.columns(2)
st.title("Data Display")
models = ['Bigram','Trigram']


#sentiment compute
with fig_col1:
    st.title("Sentiment analysis")
    
    title = st.text_input('Insert sentence to compute sentiment', '') 
    
    model = st.multiselect(
        "choose from the given models", models)
    if model!=[]:
        model_index = models.index(model[0])
        result = compute_sentiment(n = model_index,sentence=title)
        res = ''
        if result==0:
            res = 'Negative'
        elif result ==1:
            res = 'Positive'
            
        st.write('The sentence is:', res)
    
with fig_col2:
    st.title("Data Visualizations")
    selectHashTag()
    st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Section Break</p>", unsafe_allow_html=True)
    selectLocAndAuth()
wordCloud()
with st.expander("Show More Graphs"):
    stBarChart()
    langPie()









