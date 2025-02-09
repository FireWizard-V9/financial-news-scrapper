from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.tavily import TavilyTools
from phi.tools.crawl4ai_tools import Crawl4aiTools
from moneycontrol import moneycontrol_api as mc  
from dotenv import load_dotenv
import os
import json


load_dotenv()


groq_model = Groq(id="deepseek-r1-distill-llama-70b")

#  Agent 1: Web Search Agent for IPO insights
web_search_agent = Agent(
    name="IPO Web Search Agent",
    role="Searches the web for IPO listings, trends, and insights based on user queries.",
    model=groq_model,
    tools=[TavilyTools()],
    instructions=[
        "Search for upcoming IPOs in India, IPO market trends, and recent IPO performance.",
        "Provide results with sources, focusing on insider reports and financial news.",
    ],
    show_tool_calls=True,
    markdown=True,
)

#  Agent 2: Scraper Agent for extracting IPO details
scrape_agent_1 = Agent(
    name="IPO Scraper Agent",
    role="Extracts IPO details such as company name, price, size, listing date, and market impact.",
    model=groq_model,
    tools=[Crawl4aiTools()],
    instructions=[
        "Extract IPO-related information from structured financial websites.",
        "Focus on company name, IPO price, issue size, listing date, and subscription data.",
    ],
    show_tool_calls=True,
    markdown=True,
)

#  Agent 3: MoneyControl API Agent for IPO News
class MoneyControlNewsAgent:
    def fetch_ipo_news(self):
        """Fetch latest IPO news from MoneyControl API and filter for IPO-related news."""
        try:
            all_news = mc.get_news()  
            print("\n📝 Raw API Response:", all_news)  

            
            if isinstance(all_news, dict):
                all_news = [all_news]

            
            if not isinstance(all_news, list):
                return f"Unexpected response format: {type(all_news)}"

           
            ipo_news = [news for news in all_news if "IPO" in news.get("Title:", "")]

            return ipo_news if ipo_news else "No IPO-related news found."
        except Exception as e:
            return f"Error fetching IPO news: {str(e)}"


moneycontrol_news_agent = MoneyControlNewsAgent()


def fetch_all_ipo_data():
    print("\n🔵 Running IPO Agents...")

    print("\n🔍 Fetching IPO-related news from MoneyControl API...")
    ipo_news = moneycontrol_news_agent.fetch_ipo_news()

    print("\n🌐 Fetching IPO insights from Web Search Agent...")
    web_search_results = web_search_agent.run("Latest IPO trends and analysis in India")

    print("\n📊 Extracting IPO details from Scraper Agent...")
    scraper_results = scrape_agent_1.run("Extract IPO details from financial websites")

    
    def parse_run_response(response):
        if hasattr(response, "content"):
            return response.content  
        return str(response)  

    combined_results = {
        "IPO_News_MoneyControl": ipo_news,
        "IPO_Web_Search": parse_run_response(web_search_results),
        "IPO_Scraper_Results": parse_run_response(scraper_results),
    }

    return combined_results

# ✅ Run Agents & Print Combined Output
if __name__ == "__main__":
    all_ipo_data = fetch_all_ipo_data()
    print("\n📢 **Final Combined IPO Report:**")
    print(json.dumps(all_ipo_data, indent=4, ensure_ascii=False))  
