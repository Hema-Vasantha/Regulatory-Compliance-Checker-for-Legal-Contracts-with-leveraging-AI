import streamlit as st
import pdfplumber
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + " "
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        st.error("Failed to extract text from the PDF file.")
    return text

# Function to retrieve additional information about clauses from an external source
def retrieve_additional_info(clause_name):
    external_data = {
        "Arbitration Clause": "Arbitration clauses help resolve disputes without litigation.",
        "Confidentiality Clause": "Confidentiality clauses ensure sensitive information remains protected.",
        "Payment Clause": "Payment clauses outline when and how payments should be made.",
        # Add more clauses and their descriptions as needed
    }
    return external_data.get(clause_name, "No additional information available.")

# Function to extract main key clauses based on keywords and provide descriptions
def extract_key_clauses(text):
    keywords = {
        "arbitration": "Arbitration Clause",
        "assignment": "Assignment Clause",
        "cancellation": "Cancellation Clause",
        "change control": "Change Control Clause",
        "choice of law": "Choice of Law Clause",
        "confidentiality": "Confidentiality Clause",
        "conflicts of interest": "Conflicts of Interest Clause",
        "data protection": "Data Protection and Privacy Clause",
        "dispute resolution": "Dispute Resolution Clause",
        "exclusion": "Exclusion Clause",
        "escalation": "Escalation Clause",
        "force majeure": "Force Majeure Clause",
        "indemnity": "Indemnity Clause",
        "intellectual property": "Intellectual Property (IP) Clause",
        "liability limitation": "Liability Limitation Clause",
        "penalty": "Penalty Clause",
        "non-compete": "Non-Compete Clause",
        "payment": "Payment Clause",
        "severability": "Severability Clause",
        "statute of limitations": "Statute of Limitations Clause",
        "subcontracting": "Subcontracting Clause",
        "termination for convenience": "Termination for Convenience Clause",
        "warranty": "Warranty Clause"
    }
    
    clauses = []
    for keyword, clause_name in keywords.items():
        if keyword in text.lower():
            additional_info = retrieve_additional_info(clause_name)
            clauses.append((clause_name, additional_info))  # Append clause name and description
    
    return clauses, list(keywords.values())  # Return found clauses and all possible clauses


# Function to identify compliance issues based on keywords
def identify_compliance_issues(text):
    compliance_keywords = [
        'confidentiality', 
        'data protection', 
        'indemnity', 
        'liability', 
        'force majeure', 
        'payment',
        'audit',
        'regulation',
    ]
    
    issues_found = []
    for keyword in compliance_keywords:
        if keyword in text.lower():
            issues_found.append(keyword)

    return issues_found


# Function to calculate total contract analysis score out of 100
def calculate_total_score(clauses, all_clauses):
    scores = {
        clause: 4 if clause not in [
            "Confidentiality Clause", 
            "Data Protection and Privacy Clause", 
            "Dispute Resolution Clause", 
            "Force Majeure Clause", 
            "Indemnity Clause", 
            "Liability Limitation Clause", 
            "Payment Clause", 
            "Warranty Clause"] else 8
        for clause in all_clauses
    }

    total_score = sum(scores[clause] for clause, _ in clauses if clause in scores)
    
    max_score = sum(scores.values())
    normalized_score = (total_score / max_score) * 100 if max_score > 0 else 0
    
    return normalized_score, total_score, len(clauses), max_score, scores

# Function to identify contract type with explanation
def identify_contract_type(text):
    if 'lease' in text.lower():
        return 'Lease Agreement', 'The contract contains terms related to leasing properties or assets.'
    elif 'service' in text.lower():
        return 'Service Agreement', 'The contract mentions services provided by one party to another.'
    elif 'partnership' in text.lower():
        return 'Partnership Agreement', 'The contract includes terms indicating collaboration or partnership.'
    else:
        return 'Unknown', 'The contract does not contain sufficient keywords to identify its type.'


# Function to provide recommendations based on identified clauses
def generate_recommendations(key_clauses):
    recommendations = []
    
    for clause_name, _ in key_clauses:
        if clause_name == 'Confidentiality Clause':
            recommendations.append("Ensure that the confidentiality clause aligns with current data protection regulations.")
        
        elif clause_name == 'Payment Clause':
            recommendations.append("Review payment terms to ensure they are clear and enforceable.")
        
        elif clause_name == 'Indemnity Clause':
            recommendations.append("Consider specifying the scope of indemnification clearly.")
        
        elif clause_name == 'Force Majeure Clause':
            recommendations.append("Ensure that force majeure events are well-defined.")
        
       # Add more recommendations as needed for other clauses
    
    return recommendations



# Streamlit UI
st.title("Regulatory Compliance Checker with RAG")
st.sidebar.title("Upload Contract/File")
st.write("This is a Streamlit app that uses Retrieval Augmented Generation (RAG) to analyze contracts.")
submit_button = st.sidebar.button("Analyze the Contract")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.success("File successfully uploaded!")  
    
    extracted_text = extract_text_from_pdf(uploaded_file)

    if submit_button:  
        key_clauses, all_clauses = extract_key_clauses(extracted_text)
        # Identify compliance issues
        compliance_issues = identify_compliance_issues(extracted_text)

        if key_clauses:
            st.subheader("Extracted Key Clauses:")
            for clause_name, description in key_clauses:
                st.write(f"{clause_name}:** {description}")

            total_score, raw_score, num_clauses, max_score, scores = calculate_total_score(key_clauses, all_clauses)

            st.write(f"*Total Contract Analysis Score:* {total_score:.2f} out of *100*")

            description = (
                f"The total score is calculated based on the presence of {num_clauses} key clauses "
                f"identified in your contract. The maximum possible score is {max_score}, "
                f"and your contract achieved a raw score of {raw_score}. This results in a normalized score of {total_score:.2f}."
            )
            st.write(description)

            contract_type, explanation = identify_contract_type(extracted_text)
            st.write(f"*Contract Type:* {contract_type}")
            st.write(f"*Explanation:* {explanation}")
            
            
            # Display compliance issues found
            if compliance_issues:
                st.subheader("Compliance Issues Identified:")
                for issue in compliance_issues:
                    st.write(f"- *{issue.capitalize()}*")

            # Generate and display recommendations based on identified clauses
            recommendations = generate_recommendations(key_clauses)
            if recommendations:
                st.subheader("Recommendations:")
                for recommendation in recommendations:
                    st.write(f"- {recommendation}")

            st.sidebar.success("Analysis completed successfully!")  
        
        else:
            st.warning("No key clauses found.")
