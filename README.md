# Global-News-Topic-Tracker
Scrape Google News and summarize trending topics using LLMs

# 📄 Project Documentation: Global News Topic Tracker

## 📝 Overview
**Global News Topic Tracker** is a **Streamlit-based web application** that fetches trending news articles from the **Google News RSS feed**.  
This version focuses only on **fetching and displaying the latest news** and allows the user to **download them as a plain text file (.txt)**.

---

## 🔧 Tech Stack
- **Streamlit** (UI Framework)  
- **Python** (Backend Logic)  
- **Google News RSS Feed** (Data Source)  
- **BeautifulSoup4** (HTML/XML Parsing)  
- **Requests, re** (Utilities)  

---

## 🚀 Features
- Select number of news articles to fetch (**5 to 15**)  
- View the latest **headlines with descriptions**  
- **Download** the articles as a plain text file  

---

## 🖥️ How It Works
1. The app fetches articles from the **Google News RSS feed**.  
2. Titles and HTML-cleaned descriptions are extracted using **BeautifulSoup**.  
3. User selects how many articles to fetch using a **slider**.  
4. The articles are **displayed** on the Streamlit interface.  
5. A **download button** generates and saves the news to a `.txt` file.  

---

## 🐞 Issues Faced and Fixes
- ❌ **Summary being generated again on clicking download button**  
  ✅ Fixed by using `st.session_state` to cache the summary.  

- ❌ **Summary output showing bullet points instead of single paragraph**  
  ✅ Fixed by modifying the **prompt** to instruct the LLM clearly.  

- ❌ **'clean_summary' not defined error**  
  ✅ Removed unused variable and corrected logic.  

- ❌ **Unexpected reruns on download**  
  ✅ Refactored the code to avoid placing generation logic inside UI elements.  

---

## 📌 Final Notes
This version **excludes summarization** and focuses only on **collecting and downloading the latest trending news**.  
It serves as a **lightweight and effective way** to monitor news trends directly via **RSS feeds**.  

---

## ▶️ Run Instructions
1. **Install requirements**:
   ```bash
   pip install streamlit beautifulsoup4 nltk requests
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run news_app.py
   ```
