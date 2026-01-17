import asyncio
from app.services.content_service import content_service

async def test():
    test_roadmap = [
        {
            "title": "Module 1",
            "description": "Test",
            "resources": [{"title": "Example", "url": "https://example.com"}]
        }
    ]
    print("Fetching content for Rust Wikipedia...")
    result = await content_service.get_roadmap_content(test_roadmap)
    print("Result:")
    for m in result:
        print(f"Module: {m['title']}")
        for r in m['readings']:
            print(f"Resource: {r['title']}")
            print(f"Content Length: {len(r['content'])}")
            print(f"Content Preview: {r['content'][:200]}...")

if __name__ == "__main__":
    asyncio.run(test())
