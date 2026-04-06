import requests
from bs4 import BeautifulSoup

class SearchTool:
    def __init__(self):
        # Professional headers to avoid being blocked by websites
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        self.results = []

    def search(self, query):
        """Fetches live search results from DuckDuckGo."""
        try:
            response = requests.post(
                "https://html.duckduckgo.com/html/",
                data={"q": query},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            self.results = []

            # Extracting the top 5 results to keep the UI clean
            for r in soup.select(".result")[:5]:
                link = r.select_one(".result__a")
                snippet = r.select_one(".result__snippet")
                if link:
                    self.results.append({
                        "title": link.get_text(strip=True),
                        "url": link.get("href"),
                        "snippet": snippet.get_text(strip=True) if snippet else ""
                    })
            return self.results
        except Exception as e:
            return [{"title": "Search Error", "url": "", "snippet": str(e)}]

    def scrape(self, url):
        """Extracts text content from a URL for AI analysis."""
        try:
            page = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(page.text, "html.parser")
            content = []
            for tag in soup.find_all(["h1", "h2", "h3", "p", "li"]):
                text = tag.get_text(strip=True)
                if text and len(text) > 50:
                    content.append(text)
            return "\n\n".join(content[:15]) # Return first 15 chunks
        except Exception as e:
            return f"Could not scrape: {e}"