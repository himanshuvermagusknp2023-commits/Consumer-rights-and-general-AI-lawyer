"""
NyayaSetu - Legal Drafting Studio
Generates structured, professional, ready-to-dispatch legal documents:
1. Formal Legal Notice (Demand Notice with 15-Day Cure Window)
2. Consumer Complaint Petition under Section 35 CPA 2019 (for e-Daakhil / DCDRC)
3. National Consumer Helpline (NCH / INGRAM) Filing Brief
4. WhatsApp / Email Formal Escalation Message
"""

from typing import Dict, Any
from datetime import datetime

def draft_legal_notice(case: Dict[str, Any]) -> str:
    today_str = datetime.now().strftime("%d %B, %Y")
    amount = case.get("principal_claim_amount", 0)
    category = case.get("category", "ecommerce_defective_goods")
    respondent = case.get("respondent", "Opposite Party")
    summary = case.get("dispute_summary", "Dispute regarding non-refund and deficiency in service.")
    
    # Specific statutory ground based on category
    if category == "tenancy_deposit":
        statutory_ground = (
            "Under Section 108(m) of the Transfer of Property Act, 1882 read with established Indian tenancy jurisprudence "
            "and the Model Tenancy Act, the security deposit is a trust amount refundable within 30 days of vacating. "
            "The lessee is not liable for reasonable wear and tear, and any unilateral deduction without itemized contractor "
            "bills and mutual verification constitutes unauthorized retention, breach of contract, and unjust enrichment "
            "under Section 70 and Section 73 of the Indian Contract Act, 1872."
        )
    elif category == "airline_flight_refund":
        statutory_ground = (
            "Under the Directorate General of Civil Aviation (DGCA) Civil Aviation Requirements (CAR), Section 3, Series M, "
            "Part IV, and the landmark Supreme Court ruling in Pravasi Legal Cell vs. Union of India (2020), an airline is "
            "statutorily mandated to refund cancelled flights directly into the original mode of payment. Forcing a credit shell "
            "or travel voucher without explicit consent constitutes a direct Deficiency in Service under Section 2(11) and an "
            "Unfair Trade Practice under Section 2(47) of the Consumer Protection Act, 2019."
        )
    elif category == "edtech_coaching_fee":
        statutory_ground = (
            "Under the CCPA Guidelines for Prevention of Unfair Trade Practices in Coaching Sector (2024) and established "
            "NCDRC precedents (including FIITJEE Ltd. vs. Minathi Nayak), non-refundable advance fee clauses are legally void "
            "and unconscionable under Section 2(46) of the Consumer Protection Act, 2019. Retention of unearned course fees "
            "for services not availed constitutes an Unfair Trade Practice."
        )
    elif category == "unpaid_freelance_salary":
        statutory_ground = (
            "Under Section 70 and Section 73 of the Indian Contract Act, 1872, having received, accepted, and utilized the "
            "contracted deliverables/work, you are under a strict statutory and contractual obligation to release the agreed dues. "
            "Wrongful withholding of earned remuneration constitutes wilful breach of contract, unjust enrichment, and actionable civil liability."
        )
    else:
        statutory_ground = (
            "Under Section 2(10), Section 2(11), and Section 2(47) of the Consumer Protection Act, 2019, supplying defective goods "
            "and refusing timely refund/replacement within statutory periods constitutes Gross Deficiency in Service and Unfair Trade Practice, "
            "attracting punitive liability under Section 39 and Section 85 of the Act."
        )

    notice_text = f"""================================================================================
FORMAL LEGAL DEMAND NOTICE (WITHOUT PREJUDICE)
DISPATCHED VIA: REGISTERED POST WITH A.D. / SPEED POST & OFFICIAL EMAIL
================================================================================

DATE: {today_str}

TO:
{respondent}
[Full Registered Address / Corporate Office / Residential Address]
Email: [Official Email / Nodal Grievance Officer]

FROM:
[Complainant / Aggrieved Citizen Name]
[Residential Address / Contact Phone / Email]

SUBJECT:
DEMAND NOTICE FOR IMMEDIATE REFUND OF INR {amount:,}/- WITH ACCRUED INTEREST
AND COMPENSATION FOR DEFICIENCY IN SERVICE, WRONGFUL RETENTION, AND UNFAIR TRADE PRACTICE.

SIR / MADAM,

Under explicit instructions and on behalf of my client / self, the present Legal Notice is hereby served upon you:

1. FACTUAL BACKGROUND & TRANSACTION DETAILS:
   a) That the Claimant entered into a valid and lawful commercial/tenancy/service transaction with you, wherein full payment/deposit of INR {amount:,}/- was duly remitted.
   b) {summary}
   c) That despite multiple written communications, emails, and follow-ups, you have wilfully failed, neglected, and refused to remediate the defect / return the legitimate funds due to the Claimant.

2. STATUTORY VIOLATIONS & LEGAL GROUNDS:
   {statutory_ground}

3. WRONGFUL RETENTION & DAMAGES:
   By virtue of your arbitrary conduct, the Claimant has suffered severe financial distress, inconvenience, and mental agony. You have illegally retained money that does not belong to you, depriving the Claimant of its rightful use.

4. REQUISITE DEMANDS & 15-DAY CURE NOTICE:
   You are hereby formally called upon to:
   i. Immediately refund the principal amount of INR {amount:,}/- (Indian Rupees {amount:,} only) into the Claimant's designated bank account within 15 (FIFTEEN) DAYS of the receipt of this Notice;
   ii. Pay interest calculated at the rate of 12% per annum from the date the amount fell due until the date of actual payment;
   iii. Pay an amount of INR 15,000/- towards damages for mental harassment and costs incurred in issuing this formal notice.

TAKE NOTICE that if you fail to comply with the legitimate demands set forth above within the stipulated period of 15 days, the Claimant shall be constrained to institute appropriate legal proceedings against you, including filing a formal Consumer Complaint under Section 35 of the Consumer Protection Act, 2019 before the Competent District Consumer Disputes Redressal Commission / Civil Court of competent jurisdiction, entirely at your sole risk, cost, and consequences.

A copy of this Legal Notice is retained in records for future legal proceedings.

Yours faithfully,

_____________________________
[Complainant / Authorized Signatory]
Enclosures:
1. Proof of Payment / Bank Statement
2. Written Agreement / Booking Confirmation
3. Relevant WhatsApp / Email Communication Records
================================================================================"""
    return notice_text

def draft_consumer_complaint_petition(case: Dict[str, Any]) -> str:
    amount = case.get("principal_claim_amount", 0)
    category = case.get("category", "ecommerce_defective_goods")
    respondent = case.get("respondent", "Opposite Party")
    summary = case.get("dispute_summary", "Deficiency in service and unfair trade practice.")

    petition = f"""BEFORE THE HON'BLE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION
AT: [DISTRICT NAME, STATE]

CONSUMER COMPLAINT NO. ________ / {datetime.now().year}
(Under Section 35 of the Consumer Protection Act, 2019)

IN THE MATTER OF:
[Complainant Name]
S/o or D/o ________________
Residing at: [Complete Address]
Contact: [Mobile & Email]                                ... COMPLAINANT

VERSUS

{respondent}
Having Office at: [Complete Registered Address]
Represented by its Authorized Signatory/Manager         ... OPPOSITE PARTY

MEMORANDUM OF COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019

MOST RESPECTFULLY SHOWETH:

1. PARTICULARS OF PARTIES & JURISDICTION:
   The Complainant is a 'Consumer' within the meaning of Section 2(7) of the Consumer Protection Act, 2019. The Opposite Party is a service provider / seller / trader. The transaction took place within the territorial jurisdiction of this Hon'ble Commission, and the total claim amount is below INR 50,00,000/-, conferring complete pecuniary jurisdiction under Section 34 of the Act.

2. BRIEF FACTS OF THE CASE:
   a) The Complainant availed services / purchased goods from the Opposite Party for a total consideration of INR {amount:,}/-.
   b) {summary}
   c) The Opposite Party failed to honor warranty/return/refund obligations, despite service of a formal 15-day Demand Notice dated [Notice Date].

3. DEFICIENCY IN SERVICE & UNFAIR TRADE PRACTICE:
   The acts and omissions of the Opposite Party constitute 'Deficiency in Service' as defined under Section 2(11) and 'Unfair Trade Practice' under Section 2(47) of the Act.

4. PRAYER / RELIEFS SOUGHT:
   It is therefore most respectfully prayed that this Hon'ble Commission may be pleased to:
   a) Direct the Opposite Party to refund the principal amount of INR {amount:,}/- along with interest @ 12% p.a.;
   b) Award compensation of INR 25,000/- towards mental harassment, emotional trauma, and financial loss;
   c) Award litigation costs of INR 10,000/-;
   d) Pass any other order deemed fit in the interest of justice.

PLACE: _____________________
DATE:  _____________________                           COMPLAINANT IN PERSON

VERIFICATION:
I, the Complainant above named, do hereby verify that the contents of paragraphs 1 to 4 are true and correct to my personal knowledge. Verified at [City] on this day of {datetime.now().strftime("%B, %Y")}.

DEPONENT
"""
    return petition

def draft_nch_grievance(case: Dict[str, Any]) -> str:
    amount = case.get("principal_claim_amount", 0)
    respondent = case.get("respondent", "Opposite Party")
    summary = case.get("dispute_summary", "Unfair trade practice & refund refusal.")

    return f"""NATIONAL CONSUMER HELPLINE (NCH 1915 / INGRAM) GRIEVANCE SUBMISSION:
------------------------------------------------------------------------
Company/Entity Name : {respondent}
Category            : Consumer Grievance / Non-Refund / Deficiency in Service
Transaction Value   : INR {amount:,}/-
Grievance Brief     :
{summary}. Despite repeated follow-ups and service of a 15-day demand notice, the company has refused to process the legitimate refund of INR {amount:,}/-. This amounts to Deficiency in Service under Section 2(11) and Unfair Trade Practice under Section 2(47) of the Consumer Protection Act, 2019.

Relief Sought       :
Immediate refund of INR {amount:,}/- with interest, and closure of unauthorized deductions.
Attachments Ready   : Tax Invoice / Rent Agreement, Payment Slips, Written Email & Chat Rejection Records.
"""

def draft_whatsapp_escalation(case: Dict[str, Any]) -> str:
    amount = case.get("principal_claim_amount", 0)
    category = case.get("category", "ecommerce_defective_goods")

    if category == "tenancy_deposit":
        return f"""Dear Landlord,
I am writing regarding the return of my security deposit of ₹{amount:,} for the flat vacated on [Handover Date].

As per Indian tenancy law and the Transfer of Property Act (Sec 108m), ordinary wear & tear is the owner's responsibility and cannot be deducted from the security deposit. Any repair deduction requires verified contractor GST invoices, which have not been provided.

Please transfer the balance of ₹{amount:,} to my UPI/account [UPI ID] within 48 hours. If unresolved, I will be constrained to dispatch a formal statutory Legal Notice and initiate proceedings before the Rent Authority / Legal Services Authority (Lok Adalat). Hoping for an amicable resolution."""
    else:
        return f"""Dear Customer Escalation Team / Nodal Officer,
Ref: Order / Booking / Reference ID: [ID]
Disputed Amount: ₹{amount:,}

Despite multiple follow-ups, my request for refund of ₹{amount:,} remains unresolved. Please note that under the Consumer Protection Act, 2019 (Sections 2(11) and 2(47)), failure to refund defective goods / cancelled services within statutory timelines constitutes Deficiency in Service.

I request you to release the refund within 48 hours. In the absence of confirmation, I will be lodging a formal complaint with the National Consumer Helpline (NCH - 1915) and filing an e-complaint on the e-Daakhil portal.

Looking forward to your swift resolution."""
