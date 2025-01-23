import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
import re

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to extract text from images using OCR
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

# Function to extract key clauses based on keywords
def extract_key_clauses(text):
    keywords = ["confidentiality", "indemnification", "termination", "payment", "liability"]
    clauses = []
    sentences = re.split(r'(?<=[.!?]) +', text)  # Split into sentences
    for sentence in sentences:
        if any(keyword.lower() in sentence.lower() for keyword in keywords):
            clauses.append(sentence.strip())
    return clauses

# Function to calculate contract analysis score
def calculate_contract_score(clauses):
    score = 0
    max_score = len(clauses) * 10  # Assuming each clause can contribute up to 10 points

    for clause in clauses:
        if "confidentiality" in clause.lower():
            score += 10  # Full points for confidentiality clause
        elif "indemnification" in clause.lower():
            score += 8   # Slightly less for indemnification
        # Add more conditions for other clauses...

    return (score / max_score) * 100 if max_score > 0 else 0  # Return score as a percentage

# Function to identify contract type
def identify_contract_type(text):
    if "lease" in text.lower():
        return "Lease Agreement"
    elif "service" in text.lower():
        return "Service Agreement"
    elif "partnership" in text.lower():
        return "Partnership Agreement"
    # Add more conditions as needed...
    else:
        return "Unknown"

# Streamlit UI
st.title("Regulatory Compliance Checker")
st.sidebar.title("Upload contract/file")
st.write("This is a Streamlit app to show key clauses like essential provisions in contracts, agreements, or other legal documents that define the rights, obligations, and responsibilities of the parties involved.")
submit_button=st.sidebar.button("Submit")
#st.sidebar.file_uploader("pick a file" type=["pdf","docx","txt"])

contract = st.file_uploader("Upload a PDF or Image", type=["pdf", "jpg", "jpeg", "png"])


if contract is not None:
    st.sidebar.success("File successfully uploaded!")  # Show success message after file upload
    
    # Check file type and extract text accordingly
    if contract.type == "application/pdf":
        extracted_text = extract_text_from_pdf(contract)
        
    else:
        extracted_text = extract_text_from_image(contract)

    # Display extracted text (optional)
    st.text_area("Extracted Text", extracted_text, height=300)

    if submit_button:  # Process the file upon clicking the Submit button
        key_clauses = extract_key_clauses(extracted_text)

        if key_clauses:
            st.subheader("Extracted Key Clauses:")
            for i, clause in enumerate(key_clauses, start=1):
                st.write(f"{clause}")  # Display clauses as numbered points

            # Calculate contract analysis score
            contract_score = calculate_contract_score(key_clauses)
            st.write(f"**Contract Analysis Score:** {contract_score:.2f}%")

            # Identify contract type
            contract_type = identify_contract_type(extracted_text)
            st.write(f"**Contract Type:** {contract_type}")

            st.sidebar.success("Data successfully saved!")  # Show success message after processing
        
        else:
            st.warning("No key clauses found.")
