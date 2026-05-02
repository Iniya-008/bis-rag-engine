import os
import json
import re
try:
    import pdfplumber
except ImportError:
    print("pdfplumber not installed. Please install it using pip.")
    pdfplumber = None

def extract_text_from_pdf(pdf_path):
    if not pdfplumber:
        return ""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def parse_standards_text(text):
    """
    Parser to extract standard ID and Description from the real BIS SP 21 PDF.
    Splits the document based on 'IS <number>' patterns.
    """
    standards = []
    
    # Clean up whitespace and line breaks
    text = re.sub(r'\s*\n\s*', ' ', text)
    
    # Regex to find standard numbers like "IS 456 : 2000" or "IS 383: 1970"
    # We split the text by the "IS " prefix to get chunks
    chunks = re.split(r'(?=IS\s+\d+)', text)
    
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk.startswith("IS"):
            continue
            
        # Try to extract the ID and the description
        # Matches "IS 456: 2000", "IS 2185 (Part 2): 1983", etc.
        match = re.match(r'(IS\s+\d+(?:\s*\(.*?\))?(?:\s*:\s*\d+)?)\s*(.*)', chunk)
        if match:
            std_id = match.group(1).strip()
            description = match.group(2).strip()
            
            # Use the first sentence or so as title, or just duplicate description if no clear title
            title_match = re.split(r'\.|\,', description, 1)
            title = title_match[0].strip() if title_match else std_id
            
            # Only keep chunks that actually look like real standards with some text
            if len(description) > 10:
                standards.append({
                    "id": std_id,
                    "title": title,
                    "description": description[:1000] # Limit length to prevent massive chunks
                })
                
    return standards

def process_all_pdfs(data_dir):
    all_standards = []
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created {data_dir}. Please place BIS PDFs there.")
        return all_standards

    for filename in os.listdir(data_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(data_dir, filename)
            print(f"Processing {filename}...")
            text = extract_text_from_pdf(pdf_path)
            standards = parse_standards_text(text)
            all_standards.extend(standards)
            print(f"Extracted {len(standards)} standards from {filename}")
    
    return all_standards

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    standards = process_all_pdfs(data_dir)
    
    if standards:
        output_path = os.path.join(base_dir, "parsed_standards.json")
        with open(output_path, 'w') as f:
            json.dump(standards, f, indent=4)
        print(f"Saved {len(standards)} standards to {output_path}")
    else:
        print("No standards extracted. Ensure data/ folder contains properly formatted PDFs.")
