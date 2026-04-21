import sys
from pypdf import PdfReader

try:
    reader = PdfReader("تعليمات و ضوابط كتابة بحث التخرج.pdf")
    text = ""
    for idx, page in enumerate(reader.pages):
        text += f"\n--- Page {idx+1} ---\n"
        page_text = page.extract_text()
        if page_text:
            text += page_text
    
    with open("guidelines.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully extracted text to guidelines.txt")
except Exception as e:
    print(f"Error reading PDF: {e}")
