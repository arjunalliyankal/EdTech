
import asyncio
import sys
import os
import time

# Add backend to path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

from app.services.content_service import ContentService

async def test_content_service_parallel():
    print("\n--- Testing ContentService.get_roadmap_content (Parallel) ---")
    
    mock_roadmap = [
        {
            "title": "Module 1",
            "description": "Desc 1",
            "resources": [{"title": "Example 1", "url": "https://example.com"}]
        },
        {
            "title": "Module 2",
            "description": "Desc 2",
            "resources": [{"title": "Example 2", "url": "https://example.org"}]
        },
        {
            "title": "Module 3",
            "description": "Desc 3",
            "resources": [{"title": "Example 3", "url": "https://example.net"}]
        }
    ]
    
    start_time = time.time()
    try:
        result = await ContentService.get_roadmap_content(mock_roadmap)
        elapsed = time.time() - start_time
        print(f"ContentService finished in {elapsed:.2f} seconds.")
        
        print("Results:")
        for m in result:
            print(f"- {m['title']}: {len(m['readings'][0]['content'] or '')} chars")
            
    except Exception as e:
        print(f"ContentService raised exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_content_service_parallel())
