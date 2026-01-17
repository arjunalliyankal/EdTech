import sys
import os

# Create a dummy scrape.py if it doesn't exist for testing (it exists)
print(f"CWD: {os.getcwd()}")
print(f"Path: {sys.path}")

try:
    from backend.scrape import scrape_website
    print("Success: from backend.scrape")
except ImportError as e:
    print(f"Failed: from backend.scrape ({e})")
    try:
        import scrape
        print("Success: import scrape")
    except ImportError as e:
        print(f"Failed: import scrape ({e})")
