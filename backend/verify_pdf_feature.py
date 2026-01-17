
import asyncio
import sys
import os
from io import BytesIO
from pypdf import PdfWriter

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

from app.services.pdf_service import pdf_service

def create_dummy_pdf():
    buffer = BytesIO()
    p = PdfWriter()
    page = p.add_blank_page(width=100, height=100)
    # Adding text to PDF programmatically without reportlab is tricky with pypdf alone for *creation* 
    # (pypdf is mostly for manipulation), but we can just use a dummy text extraction test 
    # or rely on the Mock LLM response for structure. 
    # Actually, let's create a minimal valid PDF structure.
    p.write(buffer)
    return buffer.getvalue()

async def test_pdf_processing():
    print("\n--- Testing PDF Service ---")
    
    # 1. Test Text Extraction (Mocking input since generating a PDF with text via just pypdf is hard)
    # We will skip actual PDF *text* generation verification here and focus on the Service flow 
    # assuming valid bytes.
    # We can test the LLM generation part with a dummy string.
    
    dummy_text = """
    Introduction to Binary Search
    
    Binary search is an efficient algorithm for finding an item from a sorted list of items.
    It works by repeatedly dividing in half the portion of the list that could contain the item.
    
    Step 1: Compare target value to the middle element.
    Step 2: If unequal, determine which half target is in.
    Step 3: Repeat.
    
    Complexity is O(log n).
    """
    
    print(f"Input Text: {dummy_text[:50]}...")
    
    # 2. Test LLM Course Generation
    try:
        result = await pdf_service.generate_course_from_content(dummy_text, "test.pdf")
        import json
        print("Generated Course Structure:")
        print(json.dumps(result, indent=2))
        
        if "modules" in result and len(result["modules"]) > 0:
            print("SUCCESS: Course modules generated.")
        else:
            print("FAILURE: No modules generated.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_pdf_processing())
