"""
NyayaSetu - Case Builder Engine
Turns messy, emotional consumer complaints (English/Hinglish) into structured legal case sheets,
chronologies, evidence checklists, and missing proof audits.
"""

import re
from typing import Dict, List, Any, Optional

def extract_monetary_amount(text: str) -> Optional[int]:
    """Extracts monetary amount in INR from text."""
    patterns = [
        r'(?:₹|rs\.?|inr)\s*([\d,]+(?:\.\d+)?)',
        r'([\d,]+(?:\.\d+)?)\s*(?:rupees|rs|bucks|lakh|lacs|k)',
        r'([\d,]+)\s*(?:thousand|lakh)',
    ]
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            raw = match.group(1).replace(',', '')
            try:
                val = float(raw)
                # handle 'lakh' or 'k'
                if 'lakh' in match.group(0).lower() or 'lac' in match.group(0).lower():
                    val *= 100000
                elif 'k' in match.group(0).lower():
                    val *= 1000
                return int(val)
            except ValueError:
                continue
    # fallback find any standalone 4-6 digit number
    num_match = re.search(r'\b(\d{4,7})\b', text)
    if num_match:
        return int(num_match.group(1))
    return None

def detect_evidence_items(text: str) -> Dict[str, List[str]]:
    """Identifies which pieces of proof the user already mentions having vs what they should collect."""
    t = text.lower()
    
    proof_candidates = {
        "Payment Proof / Bank Statement / UPI Slip": ["upi", "bank statement", "transaction", "paid", "receipt", "gpay", "phonepe", "neft", "transfer"],
        "Written Agreement / Contract / Terms": ["agreement", "contract", "lease", "rent agreement", "terms", "policy", "offer letter"],
        "Written Communication / WhatsApp / Email": ["whatsapp", "chat", "email", "mail", "message", "sms", "texted"],
        "Invoice / Bill / Booking ID": ["invoice", "bill", "tax invoice", "order id", "pnr", "booking id", "ticket"],
        "Photographic / Video Evidence": ["photo", "picture", "video", "unboxing", "recording", "clip", "screenshot"],
        "Service Complaint / Ticket Number": ["ticket", "complaint number", "token", "grievance id", "reference number"]
    }
    
    found = []
    missing = []
    
    for label, keywords in proof_candidates.items():
        if any(k in t for k in keywords):
            found.append(label)
        else:
            missing.append(label)
            
    return {"found": found, "missing": missing}

def build_case_sheet(narrative: str, category: str, structured_overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Transforms raw narrative into a formal Case Sheet."""
    amount = extract_monetary_amount(narrative) or 0
    evidence = detect_evidence_items(narrative)
    
    # Calculate evidentiary readiness score
    found_count = len(evidence["found"])
    readiness_score = min(100, int((found_count / 5.0) * 100))
    if found_count == 0:
        readiness_score = 25
        
    # Heuristic extraction of Respondent
    respondent = "Opposite Party / Respondent"
    lower_t = narrative.lower()
    if "landlord" in lower_t or "owner" in lower_t:
        respondent = "Landlord / Property Owner"
    elif "flipkart" in lower_t:
        respondent = "Flipkart Internet Pvt. Ltd. & Merchant"
    elif "amazon" in lower_t:
        respondent = "Amazon Seller Services Pvt. Ltd. & Merchant"
    elif "indigo" in lower_t:
        respondent = "InterGlobe Aviation Ltd. (IndiGo Airlines)"
    elif "spicejet" in lower_t:
        respondent = "SpiceJet Ltd."
    elif "coaching" in lower_t or "institute" in lower_t:
        respondent = "Coaching Institute / Management"
    elif "client" in lower_t or "company" in lower_t or "startup" in lower_t:
        respondent = "Employer / Client Entity"

    # Break narrative into chronological points
    sentences = [s.strip() for s in re.split(r'[.\n!]+', narrative) if len(s.strip()) > 15]
    chronology = []
    for i, s in enumerate(sentences[:6], 1):
        chronology.append(f"Event {i}: {s}")

    case_data = {
        "category": category,
        "dispute_summary": sentences[0] if sentences else narrative[:120],
        "claimant_type": "Aggrieved Consumer / Tenant / Service Recipient",
        "respondent": respondent,
        "principal_claim_amount": amount,
        "interest_claimed": "12% per annum from due date until realization",
        "compensation_claimed": "₹15,000 - ₹25,000 for mental agony, harassment, and litigation expenses",
        "total_financial_exposure": amount + 15000 if amount else 25000,
        "chronology": chronology,
        "proof_available": evidence["found"],
        "missing_proof_checklist": evidence["missing"],
        "readiness_score": readiness_score,
        "raw_narrative": narrative
    }

    if structured_overrides:
        case_data.update(structured_overrides)

    return case_data

