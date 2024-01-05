import re
import PyPDF2
import os

def get_pdfs_in_folder(folder_path):
    pdfs = [f"pdfs/{f}" for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return pdfs

folder_path = "pdfs/"
pdfs = get_pdfs_in_folder(folder_path)

def get_text_from_resume(resume):
    text = ""
    pdf_reader = PyPDF2.PdfReader(resume)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def extract_valid_phone_numbers(text):
    phone_pattern = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')

    phones = phone_pattern.findall(text)

    # Filter out invalid phone numbers
    valid_phones = []
    for phone in phones:
        # Remove non-numeric characters
        numeric_phone = re.sub(r'\D', '', phone)
        
        # Check if the resulting string is a valid phone number
        if 10 <= len(numeric_phone) <= 15:
            valid_phones.append(numeric_phone)

    return valid_phones

def extract_email_and_phone_number_from_text(text):
    
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    emails = re.findall(email_pattern, text)
    phones = extract_valid_phone_numbers(text)

    years = [f"{year}" for year in range(1900, 2024)]
    phones = [phone for phone in phones if phone not in years]

    return {"emails": emails, "phones": phones}

for pdf in pdfs:
    with open(pdf, "rb") as resume:
        text = get_text_from_resume(resume)
        details = extract_email_and_phone_number_from_text(text)
        print(details)