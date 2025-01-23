import streamlit as st
import pdfplumber

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to extract main key clauses based on keywords and assign scores
def extract_key_clauses(text):
    # Define keywords and their corresponding scores
    keywords = {
        "arbitration": ("Arbitration Clause", 4),  # Normalized score contribution
        "assignment": ("Assignment Clause", 4),
        "cancellation": ("Cancellation Clause", 4),
        "change control": ("Change Control Clause", 4),
        "choice of law": ("Choice of Law Clause", 4),
        "confidentiality": ("Confidentiality Clause", 8),
        "conflicts of interest": ("Conflicts of Interest Clause", 4),
        "data protection": ("Data Protection and Privacy Clause", 8),
        "dispute resolution": ("Dispute Resolution Clause", 8),
        "exclusion": ("Exclusion Clause", 4),
        "escalation": ("Escalation Clause", 4),
        "force majeure": ("Force Majeure Clause", 8),
        "indemnity": ("Indemnity Clause", 8),
        "intellectual property": ("Intellectual Property (IP) Clause", 4),
        "liability limitation": ("Liability Limitation Clause", 8),
        "penalty": ("Penalty Clause", 4),
        "non-compete": ("Non-Compete Clause", 8),
        "payment": ("Payment Clause", 8),
        "severability": ("Severability Clause", 4),
        "statute of limitations": ("Statute of Limitations Clause", 4),
        "subcontracting": ("Subcontracting Clause", 4),
        "termination for convenience": ("Termination for Convenience Clause", 8),
        "warranty": ("Warranty Clause", 8)
    }
    
    clauses = []
    for keyword, (clause_name, score) in keywords.items():
        if keyword in text.lower():
            clauses.append((clause_name, score))  # Append tuple of clause name and its score
    
    return clauses

# Function to calculate total contract analysis score out of 100
def calculate_total_score(clauses):
    max_score = sum(score for _, score in [
        (name, score) for name, score in {
            "Arbitration Clause": 4,
            "Assignment Clause": 4,
            "Cancellation Clause": 4,
            "Change Control Clause": 4,
            "Choice of Law Clause": 4,
            "Confidentiality Clause": 8,
            "Conflicts of Interest Clause": 4,
            "Data Protection and Privacy Clause": 8,
            "Dispute Resolution Clause": 8,
            "Exclusion Clause": 4,
            "Escalation Clause": 4,
            "Force Majeure Clause": 8,
            "Indemnity Clause": 8,
            "Intellectual Property (IP) Clause": 4,
            "Liability Limitation Clause": 8,
            "Penalty Clause": 4,
            "Non-Compete Clause": 8,
            "Payment Clause": 8,
            "Severability Clause": 4,
            "Statute of Limitations Clause": 4,
            "Subcontracting Clause": 4,
            "Termination for Convenience Clause": 8,
            "Warranty Clause": 8
        }.items()
    ]) 

    total_score = sum(score for _, score in clauses)
    
    # Normalize the total score to be out of a maximum of 100
    normalized_score = (total_score / max_score) * 100 if max_score > 0 else 0
    return normalized_score

# Function to identify contract type
def identify_contract_type(text):
    if "lease" in text.lower():
        return "Lease Agreement"
    elif "service" in text.lower():
        return "Service Agreement"
    elif "partnership" in text.lower():
        return "Partnership Agreement"
    else:
        return "Unknown"


#Streamlit UI
st.title("Regulatory Compliance Checker")
st.sidebar.title("Upload contract/file")
st.write("This is a Streamlit app to show key clauses like essential provisions in contracts, agreements, or other legal documents that define the rights, obligations, and responsibilities of the parties involved.")
submit_button=st.sidebar.button("Submit")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.success("File successfully uploaded!")  
    
    # Extract text from the uploaded PDF file
    extracted_text = extract_text_from_pdf(uploaded_file)

    # Display extracted text (optional)
    st.text_area("Extracted Text", extracted_text, height=300)

    if submit_button:  
        key_clauses = extract_key_clauses(extracted_text)

        if key_clauses:
            st.subheader("Extracted Key Clauses and Scores:")
            
            # Display each clause with its corresponding score
            for i, (clause, score) in enumerate(key_clauses, start=1):
                st.write(f"{i}. {clause} - Score: {score}")

            # Calculate total normalized contract analysis score (out of 100)
            total_score = calculate_total_score(key_clauses)
            
            st.write(f"**Total Contract Analysis Score:** {total_score:.2f} out of **100**")

            # Identify contract type
            contract_type = identify_contract_type(extracted_text)
            st.write(f"**Contract Type:** {contract_type}")

            st.sidebar.success("Data successfully saved!")  
        
        else:
            st.warning("No key clauses found.")
