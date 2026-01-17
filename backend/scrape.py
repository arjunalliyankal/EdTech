import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup



        
        
        
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
    
    
    
    
    
def scrape_website(website):
    print(f"launching the browser for {website}") 
    
    # Use absolute path to the chromedriver in the aiwebscraper directory
    chrome_driver_path = r"c:\Users\arjun\inkrithackthon\aiwebscraper\chromedriver.exe"
   
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options) 
    
    try:
        driver.get(website)
        print("page loaded")
        # Wait a bit for JS to render
        time.sleep(5)
        html = driver.page_source
        
        return clean_body_content(extract_body_content(html))
    except Exception as e:
        print(f"Error scraping {website}: {e}")
        return ""
    finally:
        driver.quit()
        print("browser closed")
        
# if __name__ == "__main__":
#     website = "https://en.wikipedia.org/wiki/Hong_Kong"
#     dom_content = scrape_website(website)
#     print(dom_content)
#     #print(split_dom_content(dom_content))