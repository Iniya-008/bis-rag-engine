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
    Parser to extract standard ID, Title, and Description.
    Assumes a structured text format from the PDF like:
    ID: IS 456
    Title: Plain and Reinforced Concrete
    Description: This is the description...
    """
    standards = []
    # Regex to catch blocks of ID, Title, Description
    pattern = re.compile(r"ID:\s*(IS\s*\w+)\s*\nTitle:\s*(.*?)\s*\nDescription:\s*(.*?)(?=\nID:|\Z)", re.DOTALL)
    matches = pattern.findall(text)
    
    for match in matches:
        std_id = match[0].strip()
        title = match[1].strip()
        description = match[2].strip().replace('\n', ' ')
        standards.append({
            "id": std_id,
            "title": title,
            "description": description
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
