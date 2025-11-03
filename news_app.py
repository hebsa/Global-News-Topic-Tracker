import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import subprocess

# -------------------- Streamlit Setup -------------------- #
st.set_page_config(page_title="Global News Topic Tracker", layout="wide")

# -------------------- Utility Functions -------------------- #
def clean_html(raw_html):
    """Remove HTML tags from a string."""
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)

def fetch_google_news():
    """Fetch top Google News headlines via RSS."""
    rss_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    response = requests.get(rss_url)
    soup = BeautifulSoup(response.content, "xml")
    items = soup.findAll("item")

    articles = []
    for item in items:
        title = item.title.text.strip()
        raw_description = item.description.text if item.description else ""
        description = clean_html(raw_description).strip()
        link = item.link.text.strip() if item.link else ""
        articles.append({
            "title": title,
            "description": description,
            "link": link
        })
    return articles

def run_ollama(prompt):
    """Call the local Ollama model (e.g., mistral) for summarization."""
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        return f"❌ Ollama Error: {e.stderr.decode('utf-8', errors='replace')}"
    except FileNotFoundError:
        return "❌ Ollama not found. Please install Ollama and pull mistral model (run: ollama pull mistral)."

# -------------------- LLM Summarization -------------------- #
def summarize_trending_topics(articles):
    """Combine all article info and summarize using LLM."""
    combined_text = ""
    for i, art in enumerate(articles, 1):
        combined_text += f"{i}. {art['title']}. {art['description']}\n"

    prompt = (
        "You are an expert news analyst. Summarize the key global trends and topics "
        "from the following list of latest Google News headlines and descriptions. "
        "Write a single, coherent paragraph capturing the main themes without bullet points.\n\n"
        f"{combined_text}"
    )

    return run_ollama(prompt)

# -------------------- Streamlit UI -------------------- #
st.markdown(
    "<h1 style='color: darkblue; text-align: center;'>🌍 Global News Topic Tracker</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Scrapes Google News and summarizes trending topics using a Local LLM (Mistral via Ollama).</p>",
    unsafe_allow_html=True
)

# Fetch once per session
if "articles" not in st.session_state:
    with st.spinner("Fetching latest news..."):
        st.session_state.articles = fetch_google_news()

# Refresh Button
if st.button("🔄 Refresh News"):
    with st.spinner("Refreshing news feed..."):
        st.session_state.articles = fetch_google_news()
    st.experimental_rerun()

# Slider for number of articles
num_articles = st.slider("Select number of articles to analyze:", min_value=5, max_value=15, value=10)

articles = st.session_state.articles[:num_articles]

# Display fetched articles
if not articles:
    st.error("No news articles found.")
else:
    st.markdown(
        f"<h3 style='color: green;'>📰 Top {len(articles)} Trending Articles</h3>",
        unsafe_allow_html=True
    )

    for i, art in enumerate(articles, 1):
        st.markdown(f"<h4 style='color:#d35400;'>{i}. {art['title']}</h4>", unsafe_allow_html=True)
        st.write(art["description"])
        if art["link"]:
            st.markdown(f"[Read more]({art['link']})")
        st.markdown("<hr>", unsafe_allow_html=True)

    # Generate Summary Button
    if st.button("🧠 Summarize Trending Topics"):
        with st.spinner("Summarizing using LLM..."):
            summary = summarize_trending_topics(articles)

        st.success("✅ Summary Generated Successfully!")
        st.markdown("### 🧾 Combined Summary")
        st.write(summary)

        # Download Summary
        st.download_button(
            label="📥 Download Summary as TXT",
            data=summary,
            file_name="trending_topics_summary.txt",
            mime="text/plain"
        )
