import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Netflix Content Analysis", layout="wide")

# Title
st.title("🎬 Netflix Content Data Analysis")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("netflix_titles.csv")

df = load_data()

# Clean data
df['date_added'] = pd.to_datetime(df['date_added'])
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month
df['duration'] = df['duration'].fillna('0 min')
df[['duration_int', 'duration_type']] = df['duration'].str.extract(r'(\d+)\s*(\w+)?')
df['duration_int'] = pd.to_numeric(df['duration_int'], errors='coerce')
df['cast'] = df['cast'].fillna('')
df['director'] = df['director'].fillna('')

st.sidebar.title("Filters")
content_type = st.sidebar.multiselect("Select Type", options=df['type'].unique(), default=df['type'].unique())
df = df[df['type'].isin(content_type)]

st.markdown("### 📊 Content Type Distribution")
fig1, ax1 = plt.subplots()
sns.countplot(data=df, x='type', ax=ax1)
st.pyplot(fig1)

st.markdown("### 🗓️ Content Added Over the Years")
fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.countplot(data=df, x='year_added', hue='type', ax=ax2, order=sorted(df['year_added'].dropna().unique()))
plt.xticks(rotation=45)
st.pyplot(fig2)

st.markdown("### 🎭 Top 10 Genres")
top_genres = df['listed_in'].str.split(', ').explode().value_counts().head(10)
fig3, ax3 = plt.subplots()
top_genres.plot(kind='barh', color='skyblue', ax=ax3)
ax3.invert_yaxis()
st.pyplot(fig3)

st.markdown("### 👥 Top 10 Actors")
top_actors = df['cast'].str.split(', ').explode().value_counts().head(10)
fig4, ax4 = plt.subplots()
top_actors.plot(kind='bar', color='purple', ax=ax4)
plt.xticks(rotation=45)
st.pyplot(fig4)

st.markdown("### 🎬 Top 10 Directors")
top_directors = df['director'].str.split(', ').explode().value_counts().head(10)
fig5, ax5 = plt.subplots()
top_directors.plot(kind='bar', color='orange', ax=ax5)
plt.xticks(rotation=45)
st.pyplot(fig5)

st.markdown("### ⏱️ Movie Duration Distribution")
fig6, ax6 = plt.subplots()
sns.histplot(df[df['type'] == 'Movie']['duration_int'].dropna(), bins=30, kde=True, color='green', ax=ax6)
ax6.set_xlabel("Minutes")
st.pyplot(fig6)

st.markdown("### 📺 TV Show Seasons Distribution")
fig7, ax7 = plt.subplots()
tv_df = df[df['type'] == 'TV Show']
sns.countplot(data=tv_df, x='duration_int', color='red', order=sorted(tv_df['duration_int'].dropna().unique()), ax=ax7)
ax7.set_xlabel("Seasons")
st.pyplot(fig7)
