import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['country'] = df['country'].fillna('Unknown')
    df['listed_in'] = df['listed_in'].fillna('')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
year_filter = st.sidebar.multiselect("Select Year(s) Added", sorted(df['year_added'].dropna().unique()), default=None)
genre_filter = st.sidebar.multiselect("Select Genre(s)", sorted(set(', '.join(df['listed_in']).split(', '))), default=None)
country_filter = st.sidebar.multiselect("Select Country(ies)", sorted(set(', '.join(df['country']).split(', '))), default=None)

# Apply filters
def apply_filters(df):
    if year_filter:
        df = df[df['year_added'].isin(year_filter)]
    if genre_filter:
        df = df[df['listed_in'].apply(lambda x: any(g in x for g in genre_filter))]
    if country_filter:
        df = df[df['country'].apply(lambda x: any(c in x for c in country_filter))]
    return df

filtered_df = apply_filters(df)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🎭 Genres & Countries", "📈 Trends"])

with tab1:
    st.header("Netflix Content Type Distribution")
    fig, ax = plt.subplots()
    sns.countplot(data=filtered_df, x="type", ax=ax)
    st.pyplot(fig)

    st.subheader("Content Added Over Years")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.countplot(data=filtered_df, x="year_added", hue="type", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab2:
    st.header("Top Genres")
    genres = filtered_df['listed_in'].str.split(', ').explode()
    top_genres = genres.value_counts().head(10)
    st.bar_chart(top_genres)

    st.header("Top Countries")
    countries = filtered_df['country'].str.split(', ').explode()
    top_countries = countries.value_counts().head(10)
    st.bar_chart(top_countries)

with tab3:
    st.header("Content Duration")
    movie_df = filtered_df[filtered_df['type'] == 'Movie'].copy()
    movie_df['duration_mins'] = movie_df['duration'].str.extract(r'(\d+)').astype(float)
    fig, ax = plt.subplots()
    sns.histplot(movie_df['duration_mins'].dropna(), bins=30, ax=ax)
    ax.set_title("Movie Duration Distribution")
    st.pyplot(fig)
