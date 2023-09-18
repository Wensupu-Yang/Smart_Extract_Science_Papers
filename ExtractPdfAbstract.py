import PyPDF2
import re

def extract_abstract_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        # Initialize PDF reader
        pdf = PyPDF2.PdfReader(file)
        text = ""

        # Extract text from all pages
        for page_num in range(len(pdf.pages)):
             text += pdf.pages[page_num].extract_text()

        # Use regular expression to find the abstract
        abstract_match = re.search(r'(?i)Abstract(.*?)(\n\n|\Z)', text, re.DOTALL)
        
        if abstract_match:
            return abstract_match.group(1).strip()
        else:
            return None

pdf_path = '/Users/wen/Documents - Wensupu’s MacBook Pro/PARA/Projects/Quickly_Extract_Science_Papers-main_daveshap/input/Facer and Sriprakash - 2021 - Provincialising Futures Literacy A caution agains.pdf'
abstract = extract_abstract_from_pdf(pdf_path)
if abstract:
    print("Abstract:", abstract)
else:
    print("Abstract not found.")
