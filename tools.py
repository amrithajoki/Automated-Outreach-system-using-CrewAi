from crewai.tools import BaseTool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

class AntigravityBrowserTool(BaseTool):
    name: str = "Antigravity Browser Tool"
    description: str = (
        "A browser tool that can search for technical leads on GitHub and LinkedIn. "
        "Useful for finding specific issues, repositories, or user profiles. "
        "Input should be a search query or a specific URL."
    )

    def _run(self, query: str) -> str:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            # Simple heuristic: if query looks like a URL, visit it. Else search duckduckgo.
            if query.startswith("http"):
                url = query
            else:
                # Search GitHub via Google/DDG to find leads
                url = f"https://html.duckduckgo.com/html/?q={query} site:github.com OR site:linkedin.com"
                
            driver.get(url)
            
            # Allow some time for dynamic content
            time.sleep(3)
            
            # Extract main content (simplified)
            body = driver.find_element(By.TAG_NAME, "body").text
            
            # Limit content length to avoid confusing LLM with too much token usage
            content = body[:8000]
            
            driver.quit()
            return f"Source: {url}\n\nContent:\n{content}"
            
        except Exception as e:
            return f"Error using browser tool: {str(e)}"
