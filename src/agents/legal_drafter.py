"""
Legal Drafting System
Generates professional Pakistani legal documents from user inputs.
"""

import os
from pathlib import Path
from typing import Dict, Any
from langchain_groq import ChatGroq
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_project_root / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")


def get_llm():
    return ChatGroq(api_key=GROQ_API_KEY, model_name=LLM_MODEL, temperature=0.2, max_tokens=3000)


# ── Document templates ─────────────────────────────────────────────────────────

TEMPLATES = {

    "Legal Notice": """Draft a formal Legal Notice under Pakistani law with these details:
Sender: {sender_name}, {sender_address}
Recipient: {recipient_name}, {recipient_address}
Issue: {issue_description}
Amount/Relief Sought: {relief_sought}
Response Deadline: {deadline} days

Requirements:
- Proper legal notice format used in Pakistani courts
- Reference applicable Pakistani laws (Contract Act 1872, etc.)
- Clear demand/relief
- Consequence of non-compliance
- Professional legal language
- Include: "Without Prejudice" header
- Sign-off section for advocate/sender""",

    "Affidavit": """Draft a formal Affidavit for Pakistani courts with these details:
Deponent Name: {deponent_name}
Father/Husband Name: {parent_name}
CNIC: {cnic}
Address: {address}
Purpose of Affidavit: {purpose}
Key Facts to State: {facts}

Requirements:
- Proper affidavit format as per Pakistani courts
- Oath declaration
- Numbered paragraphs
- Verification clause
- Space for signature, thumb impression
- Notary/oath commissioner attestation section
- Reference to Qanun-e-Shahadat Order 1984""",

    "Rent Agreement": """Draft a Rent Agreement under Pakistani law with these details:
Landlord: {landlord_name}, {landlord_cnic}
Tenant: {tenant_name}, {tenant_cnic}
Property Address: {property_address}
Monthly Rent: Rs. {monthly_rent}
Advance/Security: Rs. {advance}
Duration: {duration} months
Start Date: {start_date}
Special Conditions: {special_conditions}

Requirements:
- Formal rent agreement format per Pakistani law
- Rent Control Act compliance
- Rights and obligations of both parties
- Maintenance responsibilities
- Termination clauses
- Witness signatures section
- Stamp duty notice""",

    "FIR Draft": """Draft an FIR (First Information Report) complaint for Pakistani police with:
Complainant: {complainant_name}, {complainant_address}, CNIC: {complainant_cnic}
Incident Date/Time: {incident_datetime}
Incident Location: {incident_location}
Accused (if known): {accused_details}
Description of Incident: {incident_description}
Witnesses (if any): {witnesses}
Evidence Available: {evidence}

Requirements:
- FIR format as used in Pakistani police stations
- Relevant PPC sections to invoke
- CrPC compliance
- Clear narrative of events
- Prayer/relief sought from police
- Note: This is a draft — must be submitted to SHO in person""",

    "NDA Agreement": """Draft a Non-Disclosure Agreement under Pakistani law with:
Disclosing Party: {party_one}
Receiving Party: {party_two}
Purpose of Disclosure: {purpose}
Confidential Information Type: {info_type}
Duration: {duration}
Jurisdiction: Pakistan ({city} courts)

Requirements:
- Formal NDA under Contract Act 1872 Pakistan
- Definition of confidential information
- Obligations of receiving party
- Permitted disclosures
- Return/destruction of information clause
- Remedy for breach (injunction + damages)
- Governing law: Laws of Pakistan
- Dispute resolution clause""",

    "Power of Attorney": """Draft a Power of Attorney under Pakistani law with:
Principal (Grantor): {principal_name}, CNIC: {principal_cnic}, Address: {principal_address}
Attorney (Agent): {attorney_name}, CNIC: {attorney_cnic}, Address: {attorney_address}
Powers Granted: {powers}
Specific Limitations: {limitations}
Duration: {duration}

Requirements:
- General/Special Power of Attorney format
- Powers clearly enumerated
- Limitations explicitly stated
- Revocation clause
- Registration requirements notice (if property-related)
- Witness and notary section
- Reference to relevant Pakistani laws""",

    "Petition": """Draft a legal Petition for Pakistani courts with:
Petitioner: {petitioner_name}, {petitioner_address}
Respondent: {respondent_name}, {respondent_address}
Court: {court_name}
Nature of Petition: {petition_type}
Facts of the Case: {facts}
Legal Grounds: {legal_grounds}
Relief Sought: {relief}

Requirements:
- Formal petition format for Pakistani superior/subordinate courts
- Proper cause title
- Numbered paragraphs
- Statement of facts
- Grounds for petition with legal references
- Prayer clause
- Verification
- List of accompanying documents""",

    "Contract Agreement": """Draft a Contract Agreement under Pakistani law with:
Party One: {party_one_name}, {party_one_address}
Party Two: {party_two_name}, {party_two_address}
Subject Matter: {subject_matter}
Obligations of Party One: {obligations_one}
Obligations of Party Two: {obligations_two}
Payment Terms: {payment_terms}
Duration: {duration}
Penalties for Breach: {penalties}

Requirements:
- Formal contract under Contract Act 1872
- Offer, acceptance, consideration clearly stated
- Rights and obligations of each party
- Payment schedule
- Dispute resolution clause
- Governing law: Laws of Pakistan
- Force majeure clause
- Termination conditions
- Signatures and witnesses""",
}


def get_document_fields(doc_type: str) -> Dict[str, str]:
    """Return the required fields and their labels for a document type."""
    fields_map = {
        "Legal Notice": {
            "sender_name": "Your Full Name",
            "sender_address": "Your Address",
            "recipient_name": "Recipient's Full Name",
            "recipient_address": "Recipient's Address",
            "issue_description": "Describe the Issue / Dispute",
            "relief_sought": "What Relief / Amount Do You Want?",
            "deadline": "Response Deadline (days, e.g. 15)",
        },
        "Affidavit": {
            "deponent_name": "Your Full Name (Deponent)",
            "parent_name": "Father's / Husband's Name",
            "cnic": "Your CNIC Number",
            "address": "Your Complete Address",
            "purpose": "Purpose of Affidavit",
            "facts": "Key Facts to Declare (be specific)",
        },
        "Rent Agreement": {
            "landlord_name": "Landlord's Full Name",
            "landlord_cnic": "Landlord's CNIC",
            "tenant_name": "Tenant's Full Name",
            "tenant_cnic": "Tenant's CNIC",
            "property_address": "Property / House Address",
            "monthly_rent": "Monthly Rent (Rs.)",
            "advance": "Security / Advance Amount (Rs.)",
            "duration": "Duration (months)",
            "start_date": "Start Date",
            "special_conditions": "Any Special Conditions",
        },
        "FIR Draft": {
            "complainant_name": "Your Full Name",
            "complainant_address": "Your Address",
            "complainant_cnic": "Your CNIC",
            "incident_datetime": "Incident Date & Time",
            "incident_location": "Where Did It Happen?",
            "accused_details": "Accused Name / Description (if known)",
            "incident_description": "Describe What Happened (in detail)",
            "witnesses": "Witness Names (if any)",
            "evidence": "Evidence Available",
        },
        "NDA Agreement": {
            "party_one": "Disclosing Party Name & Details",
            "party_two": "Receiving Party Name & Details",
            "purpose": "Purpose of Information Sharing",
            "info_type": "Type of Confidential Information",
            "duration": "NDA Duration (e.g. 2 years)",
            "city": "City for Jurisdiction",
        },
        "Power of Attorney": {
            "principal_name": "Principal (Grantor) Full Name",
            "principal_cnic": "Principal's CNIC",
            "principal_address": "Principal's Address",
            "attorney_name": "Attorney (Agent) Full Name",
            "attorney_cnic": "Attorney's CNIC",
            "attorney_address": "Attorney's Address",
            "powers": "Powers Being Granted",
            "limitations": "Any Limitations / Restrictions",
            "duration": "Duration (or 'Until Revoked')",
        },
        "Petition": {
            "petitioner_name": "Petitioner's Full Name",
            "petitioner_address": "Petitioner's Address",
            "respondent_name": "Respondent's Name",
            "respondent_address": "Respondent's Address",
            "court_name": "Court Name",
            "petition_type": "Type of Petition",
            "facts": "Facts of the Case",
            "legal_grounds": "Legal Grounds / Arguments",
            "relief": "Relief / Order Sought",
        },
        "Contract Agreement": {
            "party_one_name": "Party One Name",
            "party_one_address": "Party One Address",
            "party_two_name": "Party Two Name",
            "party_two_address": "Party Two Address",
            "subject_matter": "What is the Contract About?",
            "obligations_one": "Obligations of Party One",
            "obligations_two": "Obligations of Party Two",
            "payment_terms": "Payment Terms",
            "duration": "Contract Duration",
            "penalties": "Penalties for Breach",
        },
    }
    return fields_map.get(doc_type, {})


def draft_document(doc_type: str, field_values: Dict[str, str]) -> str:
    """Generate a legal document using AI."""
    if doc_type not in TEMPLATES:
        return "Document type not supported."

    template = TEMPLATES[doc_type]
    try:
        prompt = template.format(**field_values)
    except KeyError as e:
        prompt = template  # use as-is if formatting fails

    llm = get_llm()
    system = """You are an expert Pakistani legal document drafter with 20 years of experience.
Draft professional, legally sound documents compliant with Pakistani law.
Use proper legal formatting with clear headings and sections.
Always include appropriate legal references and make the document court-ready."""

    response = llm.invoke([
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ])

    disclaimer = "\n\n---\n⚠️ **Disclaimer:** This is an AI-generated draft for reference only. Have it reviewed by a qualified Pakistani lawyer before use. Legal documents may require registration, stamps, or notarization depending on their nature."
    return response.content + disclaimer
