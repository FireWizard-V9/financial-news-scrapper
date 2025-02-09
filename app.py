import streamlit as st
import backend  # Importing backend.py directly

st.set_page_config(page_title="IPO Insights", page_icon="📈", layout="wide")

# 🎨 Streamlit UI Title
st.title("📊 Real-Time IPO Insights Dashboard")

# 🚀 Fetch IPO Data from Backend
st.write("🔄 Fetching latest IPO data...")
ipo_data = backend.fetch_all_ipo_data()  # Directly calling the function

# ✅ Display IPO News from MoneyControl
st.subheader("📰 Latest IPO News from MoneyControl")
ipo_news = ipo_data.get("IPO_News_MoneyControl", "No IPO news available.")
if isinstance(ipo_news, list):
    for news in ipo_news:
        st.markdown(f"🔹 **[{news.get('Title:', 'No Title')}]({news.get('Link:', '#')})**")
else:
    st.warning(ipo_news)

# ✅ Display IPO Market Trends from Web Search
st.subheader("🌐 Market Trends & Analysis")
st.markdown(ipo_data.get("IPO_Web_Search", "No market trends available."))

# ✅ Display IPO Scraper Results
st.subheader("📊 Extracted IPO Details")
st.write(ipo_data.get("IPO_Scraper_Results", "No IPO details available."))

# 🎯 Sidebar Controls for User Interaction
st.sidebar.header("📌 Filters & Settings")
show_news = st.sidebar.checkbox("Show IPO News", value=True)
show_trends = st.sidebar.checkbox("Show Market Trends", value=True)
show_scraper = st.sidebar.checkbox("Show Extracted IPO Details", value=True)

if not show_news:
    st.empty()
if not show_trends:
    st.empty()
if not show_scraper:
    st.empty()

st.sidebar.write("🔄 Refresh the page to reload data.")
