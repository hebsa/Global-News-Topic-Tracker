import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import nltk

# Download NLTK tokenizer (needed only once)
nltk.download('punkt')

st.set_page_config(page_title="Global News Topic Tracker", layout="wide")

# Remove HTML tags from descriptions
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)

# Fetch articles from Google News RSS (Top Stories)
def fetch_news():
    rss_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    response = requests.get(rss_url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll("item")

    news_list = []
    for item in items:
        title = item.title.text.strip()
        raw_description = item.description.text
        description = clean_html(raw_description).strip()
        link = item.link.text.strip()
        news_list.append({
            "title": title,
            "description": description,
            "link": link
        })
    return news_list

# ===================== Streamlit UI ===================== #

# Main Title
st.markdown(
    "<h1 style='color: darkblue; text-align: center;'>🗞️ Global News Topic Tracker</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Fetches top Google News articles and lets you download them.</p>",
    unsafe_allow_html=True
)

# Slider for number of articles
num_articles = st.slider("Select number of news articles:", min_value=5, max_value=15, value=10)

# Fetch all articles
with st.spinner("Fetching latest news..."):
    all_articles = fetch_news()

# Limit results based on slider
articles = all_articles[:num_articles]

if not articles:
    st.error("No news articles found.")
else:
    # Section heading
    st.markdown(
        f"<h2 style='color: green;'>📰 Top {len(articles)} News Articles</h2>",
        unsafe_allow_html=True
    )

    full_text = ""
    for i, article in enumerate(articles):
        # Colored article title
        st.markdown(
            f"<h3 style='color: #d35400;'>{i+1}. {article['title']}</h3>",
            unsafe_allow_html=True
        )
        st.write(article["description"])
        st.markdown(f"[Read more]({article['link']})")
        st.markdown("<hr>", unsafe_allow_html=True)
        full_text += f"{i+1}. {article['title']}\n{article['description']}\n{article['link']}\n\n"

    # Download button
    st.download_button(
        label="📥 Download News Articles as TXT",
        data=full_text,
        file_name="top_news_articles.txt",
        mime="text/plain"
    )
