import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Display Netflix Logo
st.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=200)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['country'] = df['country'].fillna('Unknown')
    df['listed_in'] = df['listed_in'].fillna('')
    df['cast'] = df['cast'].fillna('')
    df['director'] = df['director'].fillna('')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filter Data")
year_filter = st.sidebar.multiselect("📅 Select Year(s) Added", sorted(df['year_added'].dropna().unique()), default=list(df['year_added'].dropna().unique()))
genre_filter = st.sidebar.multiselect("🎭 Select Genre(s)", sorted(set(', '.join(df['listed_in']).split(', '))), default=[])
country_filter = st.sidebar.multiselect("🌍 Select Country(ies)", sorted(set(', '.join(df['country']).split(', '))), default=[])

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

# Debug Info
st.write("Filtered DataFrame shape:", filtered_df.shape)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎭 Genres, Countries & People", "📈 Trends", "📝 Summary"])

with tab1:
    st.header("🎬 Netflix Content Type Distribution")
    if not filtered_df.empty:
        fig, ax = plt.subplots()
        sns.countplot(data=filtered_df, x="type", ax=ax)
        ax.set_title("Movies vs TV Shows")
        st.pyplot(fig)
    else:
        st.warning("No data to display. Try adjusting your filters.")

    st.subheader("🥧 Content Type Distribution (Pie Chart)")
    type_counts = filtered_df['type'].value_counts()
    if not type_counts.empty:
        fig, ax = plt.subplots()
        ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

    st.subheader("📅 Content Added Over Years")
    if not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.countplot(data=filtered_df, x="year_added", hue="type", ax=ax)
        ax.set_title("Content Added by Year")
        plt.xticks(rotation=45)
        st.pyplot(fig)

with tab2:
    st.header("🎭 Top Genres")
    genres = filtered_df['listed_in'].str.split(', ').explode()
    top_genres = genres.value_counts().head(10)
    st.bar_chart(top_genres)

    st.subheader("🥧 Top Genres (Pie Chart)")
    fig, ax = plt.subplots()
    ax.pie(top_genres, labels=top_genres.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.header("🌍 Top Countries")
    countries = filtered_df['country'].str.split(', ').explode()
    top_countries = countries.value_counts().head(10)
    st.bar_chart(top_countries)

    st.subheader("🥧 Top Countries (Pie Chart)")
    fig, ax = plt.subplots()
    ax.pie(top_countries, labels=top_countries.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.header("👤 Top Actors")
    actors = filtered_df['cast'].str.split(', ').explode().str.strip()
    top_actors = actors[actors != ''].value_counts().head(10)
    st.bar_chart(top_actors)

    st.header("🎬 Top Directors")
    directors = filtered_df['director'].str.split(', ').explode().str.strip()
    top_directors = directors[directors != ''].value_counts().head(10)
    st.bar_chart(top_directors)

with tab3:
    st.header("⏱️ Movie Duration Distribution")
    movie_df = filtered_df[filtered_df['type'] == 'Movie'].copy()
    movie_df['duration_mins'] = movie_df['duration'].str.extract(r'(\d+)').astype(float)
    if not movie_df['duration_mins'].dropna().empty:
        fig, ax = plt.subplots()
        sns.histplot(movie_df['duration_mins'].dropna(), bins=30, ax=ax)
        ax.set_title("Movie Duration (in minutes)")
        st.pyplot(fig)

    st.header("📺 TV Show Seasons Distribution")
    tv_df = filtered_df[filtered_df['type'] == 'TV Show'].copy()
    tv_df['seasons'] = tv_df['duration'].str.extract(r'(\d+)').astype(float)
    if not tv_df['seasons'].dropna().empty:
        fig, ax = plt.subplots()
        sns.histplot(tv_df['seasons'].dropna(), bins=15, ax=ax)
        ax.set_title("Number of Seasons")
        st.pyplot(fig)

with tab4:
    st.header("📅 Gantt Chart – Project Timeline")
    gantt_data = pd.DataFrame({
        "Task": [
            "Project Initiation", "Data Collection", "Data Cleaning & Preprocessing",
            "Exploratory Data Analysis", "Visualization & Insights", "Final Report"
        ],
        "Start": pd.to_datetime([
            "2025-07-01", "2025-07-01", "2025-07-08",
            "2025-07-10", "2025-07-15", "2025-07-18"
        ]),
        "Finish": pd.to_datetime([
            "2025-07-07", "2025-07-08", "2025-07-10",
            "2025-07-15", "2025-07-18", "2025-07-21"
        ])
    })
    gantt_fig = px.timeline(gantt_data, x_start="Start", x_end="Finish", y="Task", color="Task")
    gantt_fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(gantt_fig, use_container_width=True)

    st.header("🔍 Key Insights")
    st.markdown("""
    - **🎬 Movies dominate** Netflix’s catalog over TV Shows.
    - **📅 Most content** was added post-2016, indicating rapid growth.
    - **🌍 Top producing countries**: United States and India.
    - **🎭 Drama** is the most common genre on the platform.
    - **⏱️ Movies** are typically between **90-100 minutes** long.
    - **📺 TV Shows** mostly have **1 to 3 seasons**.
    - **👤 Prominent actors** like Anupam Kher, Om Puri frequently appear.
    - **🎬 Directors** like Raúl Campos and Marcus Raboy have directed multiple titles.
    """)
