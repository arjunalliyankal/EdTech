import trafilatura
import httpx
import logging
from typing import List, Dict
from app.services.llm_provider import llm

logger = logging.getLogger(__name__)

import asyncio
from concurrent.futures import ThreadPoolExecutor
try:
    from scrape import scrape_website
except ImportError:
    # Fallback for different path configurations
    try:
        from backend.scrape import scrape_website
    except ImportError:
        # Define dummy if missing to avoid crasing app, will use fallback
        def scrape_website(url): return None

class ContentService:
    _executor = ThreadPoolExecutor(max_workers=3)

    @staticmethod
    async def fetch_web_content(url: str) -> str:
        """
        Fetches and extracts main text from a given URL using Selenium with fallback to Trafilatura.
        """
        # Try Selenium first (as requested by user)
        try:
            loop = asyncio.get_event_loop()
            # Run blocking Selenium call in a reusable thread pool
            content = await loop.run_in_executor(ContentService._executor, scrape_website, url)
            if content and len(content) > 200:
                return content
        except Exception as e:
            logger.error(f"Selenium scraping failed for {url}: {e}")

        # Fallback to Trafilatura (faster, lighter)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
                response = await client.get(url, follow_redirects=True)
                if response.status_code == 200:
                    downloaded = response.text
                    result = trafilatura.extract(downloaded)
                    if result and len(result) > 200:
                        return result
                    
                return None
        except Exception as e:
            logger.error(f"Trafilatura scraping failed for {url}: {e}")
            return None

    @staticmethod
    async def generate_ai_overview(title: str, description: str) -> str:
        """
        Generates a detailed AI overview if web scraping fails.
        """
        prompt = f"""
        Act as an expert technical writer.
        Generate a detailed introductory overview for the topic: "{title}".
        Context: {description}
        
        Requirements:
        1. Provide a clear definition.
        2. Explain 3-4 key concepts or components.
        3. Discuss typical use cases.
        4. Keep the tone professional but accessible.
        5. Length: ~500 words.
        """
        schema = '{"content": "The full markdown or text content..."}'
        result = await llm.generate_structured(prompt, schema)
        return result.get("content", "Content generation failed.")

    @staticmethod
    async def _process_module(module: Dict) -> Dict:
        """
        Helper to process a single module: fetch content and format it.
        """
        title = module.get("title", "Untitled Topic")
        description = module.get("description", "")
        
        # Try to scrape first
        content = None
        source_url = "AI Generated"
        source_title = "AI Knowledge Base"

        if module.get("resources"):
            first_resource = module["resources"][0]
            if isinstance(first_resource, dict) and first_resource.get("url"):
                url = first_resource["url"]
                if url.startswith("http"):
                    content = await ContentService.fetch_web_content(url)
                    if content:
                        source_url = url
                        source_title = first_resource.get("title", "Web Resource")

        # Fallback to AI if no content scraped
        if not content:
            content = await ContentService.generate_ai_overview(title, description)

        return {
            "title": title,
            "description": description,
            "readings": [{
                "title": source_title,
                "url": source_url,
                "content": content
            }]
        }

    @staticmethod
    async def get_roadmap_content(roadmap: List[Dict]) -> List[Dict]:
        """
        Iterates through roadmap modules and fetches content for their resources in parallel.
        """
        tasks = [ContentService._process_module(module) for module in roadmap]
        detailed_modules = await asyncio.gather(*tasks)
        return detailed_modules

content_service = ContentService()
