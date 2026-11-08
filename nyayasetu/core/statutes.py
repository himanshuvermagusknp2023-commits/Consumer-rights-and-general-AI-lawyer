"""
NyayaSetu - Verified Indian Statutes Knowledge Base
Strictly grounded statutory references for everyday consumer and civil disputes in India.
Designed to prevent LLM hallucinations by acting as a deterministic citation anchor.
"""

from typing import Dict, List, Any

VERIFIED_STATUTES: Dict[str, Dict[str, Any]] = {
    "tenancy_deposit": {
        "domain": "Tenancy & Rental Security Deposits",
        "primary_statutes": [
            {
                "act": "Model Tenancy Act, 2021 / State Rent Control & Tenancy Norms",
                "section": "Section 10 & 13",
                "title": "Security Deposit Limits & Return Obligations",
                "summary": "Security deposit for residential premises is typically capped at two months' rent and must be returned within 30 days of the tenant vacating, after deducting legitimate undisputed arrears.",
                "rules": [
                    "Normal wear and tear (natural fading of wall paint, minor scuffs) cannot be deducted from security deposit.",
                    "Any deduction for property damage must be accompanied by itemized contractor receipts and photographic evidence.",
                    "Arbitrary forfeiture of deposit constitutes unjust enrichment and breach of contract."
                ]
            },
            {
                "act": "Transfer of Property Act, 1882",
                "section": "Section 108(m)",
                "title": "Lessee's Obligation Regarding Condition of Property",
                "summary": "The tenant is bound to keep and restore the property in as good condition as it was at commencement, reasonable wear and tear excepted.",
                "rules": [
                    "Landlord cannot claim complete repainting costs after standard tenancy without proof of willful tenant damage."
                ]
            },
            {
                "act": "Indian Contract Act, 1872",
                "section": "Section 73 & Section 70",
                "title": "Compensation for Breach of Contract / Unjust Retention",
                "summary": "Party suffering from breach is entitled to compensation for direct loss. Retaining a refundable deposit without legal justification entitles tenant to return with statutory interest.",
                "rules": [
                    "Legal demand notice must give minimum 15 days to refund before initiating formal civil proceedings."
                ]
            }
        ],
        "authorities": [
            "Rent Tribunal / Rent Authority under State Tenancy Act",
            "District Legal Services Authority (DLSA) - Lok Adalat for speedy settlement",
            "Civil Court (Small Causes Court) for recovery of money"
        ],
        "limitation_period": "3 years from the date of cause of action (vacating premises) under Limitation Act, 1963."
    },
    "ecommerce_defective_goods": {
        "domain": "E-Commerce & Defective Goods",
        "primary_statutes": [
            {
                "act": "Consumer Protection Act, 2019",
                "section": "Section 2(10)",
                "title": "Definition of Defect",
                "summary": "Any fault, imperfection or shortcoming in the quality, quantity, potency, purity or standard which is required to be maintained by or under any law.",
                "rules": [
                    "Goods received damaged or with manufacturing defects fall squarely under Section 2(10)."
                ]
            },
            {
                "act": "Consumer Protection Act, 2019",
                "section": "Section 2(11)",
                "title": "Definition of Deficiency in Service",
                "summary": "Any fault, imperfection, shortcoming or inadequacy in the quality, nature and manner of performance required to be maintained under contract or law.",
                "rules": [
                    "Refusing refund, delaying technician inspections, or closing tickets unilaterally constitutes deficiency in service."
                ]
            },
            {
                "act": "Consumer Protection Act, 2019",
                "section": "Section 2(47)",
                "title": "Unfair Trade Practice",
                "summary": "Deceptive practices including falsely representing goods as of particular standard, refusing to refund after taking payment, or misleading warranty terms.",
                "rules": [
                    "Hiding behind 'replacement only' when replacement is unfulfilled is an unfair trade practice."
                ]
            },
            {
                "act": "Consumer Protection (E-Commerce) Rules, 2020",
                "section": "Rule 5 & Rule 6",
                "title": "Liabilities of Marketplace and Inventory E-Commerce Entities",
                "summary": "Mandates appointment of a Grievance Officer, acknowledgment of complaints within 48 hours, and resolution within 1 month. Platforms facilitating payment and delivery cannot disclaim total responsibility.",
                "rules": [
                    "E-commerce platform must disclose details of seller and grievance redressal officer."
                ]
            },
            {
                "act": "Consumer Protection Act, 2019",
                "section": "Section 35",
                "title": "Manner in which Complaint may be made to District Commission",
                "summary": "A consumer can file a complaint in the District Consumer Disputes Redressal Commission (pecuniary jurisdiction up to ₹50 Lakhs) physically or electronically via e-Daakhil.",
                "rules": [
                    "Remedies under Section 39 include refund of price paid, replacement, compensation for mental harassment, and litigation costs."
                ]
            }
        ],
        "authorities": [
            "National Consumer Helpline (NCH - 1915 / INGRAM portal)",
            "District Consumer Disputes Redressal Commission (DCDRC) via e-Daakhil portal",
            "Central Consumer Protection Authority (CCPA) for class-action unfair trade practices"
        ],
        "limitation_period": "2 years from the date on which the cause of action arose (Section 69 CPA 2019)."
    },
    "edtech_coaching_fee": {
        "domain": "Coaching & EdTech Advance Fee Disputes",
        "primary_statutes": [
            {
                "act": "Consumer Protection Act, 2019",
                "section": "Section 2(46)",
                "title": "Unfair Contract",
                "summary": "A contract with unreasonable terms, including imposing unreasonable penalty or forfeiture of money on premature termination by consumer.",
                "rules": [
                    "Standard clauses stating 'Fees once paid will not be refunded under any circumstances' are unconscionable and legally void under Section 2(46)."
                ]
            },
            {
                "act": "CCPA Guidelines for Prevention of Unfair Trade Practices in Coaching Sector, 2024",
                "section": "Guideline 4 & 5",
                "title": "Prohibition of False Commitments and Advance Fee Forfeiture",
                "summary": "Coaching centres cannot misrepresent batch sizes, faculty credentials, or retain full fees when a student leaves mid-way. Must provide pro-rata refund.",
                "rules": [
                    "Mandatory pro-rata refund of unutilized course fee within 10 days of exit request."
                ]
            },
            {
                "act": "Supreme Court & NCDRC Landmark Precedents",
                "section": "FIITJEE Ltd. vs. Minathi Nayak & Brilliant Tutorials precedents",
                "title": "Forfeiture of Advance Fees Declared Illegal",
                "summary": "Courts have repeatedly ruled that educational institutions and commercial coaching centres cannot hoard entire course fees if a student withdraws.",
                "rules": [
                    "Coaching institutes are service providers amenable to Consumer Forum jurisdiction."
                ]
            }
        ],
        "authorities": [
            "District Consumer Disputes Redressal Commission (DCDRC) via e-Daakhil",
            "National Consumer Helpline (NCH - 1915)",
            "Central Consumer Protection Authority (CCPA)"
        ],
        "limitation_period": "2 years from the date of withdrawal/refund refusal."
    },
    "airline_flight_refund": {
        "domain": "Airline Delays, Cancellations & Refund Withholding",
        "primary_statutes": [
            {
                "act": "DGCA Civil Aviation Requirements (CAR)",
                "section": "Section 3, Series M, Part IV",
                "title": "Refund Obligations upon Airline Flight Cancellation",
                "summary": "When a flight is cancelled or delayed beyond specified thresholds by the airline, passenger has the absolute choice between alternate flight or immediate full refund.",
                "rules": [
                    "Refund must be made immediately if paid in cash, or within 7 days for credit/debit card transactions.",
                    "Airlines cannot forcefully lock passenger money into an airline credit shell or travel voucher without explicit written passenger consent."
                ]
            },
            {
                "act": "Supreme Court of India Ruling",
                "section": "Pravasi Legal Cell & Ors. vs. Union of India (2020)",
                "title": "Inadmissibility of Unilateral Credit Shells",
                "summary": "The Supreme Court held that passengers must receive refunds into original payment method; credit shells without consent violate statutory consumer protections.",
                "rules": [
                    "Credit shell can only be an option, never a forced default."
                ]
            },
            {
                "act": "Consumer Protection Act, 2019",
                "section": "Section 2(11) & 35",
                "title": "Deficiency of Service in Commercial Aviation",
                "summary": "Failure to provide timely refund or arbitrary cancellation entitles passenger to ticket refund plus compensation.",
                "rules": [
                    "Can be escalated to AirSewa grievance portal."
                ]
            }
        ],
        "authorities": [
            "AirSewa Portal (Ministry of Civil Aviation)",
            "DGCA Passenger Grievance Cell",
            "District Consumer Disputes Redressal Commission (DCDRC)"
        ],
        "limitation_period": "2 years under Consumer Protection Act."
    },
    "unpaid_freelance_salary": {
        "domain": "Unpaid Salary & Freelancer Contractual Dues",
        "primary_statutes": [
            {
                "act": "Indian Contract Act, 1872",
                "section": "Section 70",
                "title": "Obligation of Person Enjoying Benefit of Non-Gratuitous Act",
                "summary": "Where a person lawfully does anything for another person, not intending to do so gratuitously, and such other person enjoys the benefit thereof, the latter is bound to make compensation.",
                "rules": [
                    "Client who accepted software/design/services cannot refuse payment by delaying review or citing financial distress."
                ]
            },
            {
                "act": "Indian Contract Act, 1872",
                "section": "Section 73",
                "title": "Breach of Contract & Damages",
                "summary": "Right to claim agreed contractual amount plus interest for wrongful withholding of funds.",
                "rules": [
                    "Written agreements, email approvals, or WhatsApp confirmations constitute binding contract."
                ]
            },
            {
                "act": "MSMED Act, 2006 (if registered under Udyam)",
                "section": "Section 15 & 16",
                "title": "Mandatory 45-Day Payment & Compound Interest",
                "summary": "Buyer must pay micro/small enterprise within agreed period (max 45 days). Overdue payments attract compound interest at 3 times RBI bank rate.",
                "rules": [
                    "Direct filing available on MSME Samadhaan portal without court fee."
                ]
            },
            {
                "act": "Payment of Wages Act, 1936 & State Shops and Commercial Establishments Act",
                "section": "Applicable state shop act sections",
                "title": "Timely Disbursement of Wages",
                "summary": "Salary must be paid on or before the 7th or 10th of every month. Employer cannot withhold earned wages.",
                "rules": [
                    "Labor Commissioner / Labor Officer has summary jurisdiction for unpaid salary recovery."
                ]
            }
        ],
        "authorities": [
            "MSME Samadhaan Portal (for registered MSME/Udyam freelancers)",
            "Labor Commissioner's Office under State Shops & Establishments Act",
            "Civil Court (Summary Suit under Order XXXVII CPC) or Lok Adalat"
        ],
        "limitation_period": "3 years from the date salary/invoice became due."
    }
}

OUT_OF_SCOPE_DOMAINS = [
    {
        "domain": "Violent Crimes / Serious Criminal Offenses (Murder, Assault, POCSO, Rape, Robbery)",
        "action": "Immediate emergency escalation. Direct user to Dial 112 (Police) or nearest Police Station. Explain that AI cannot advise on criminal bail or arrest defense."
    },
    {
        "domain": "Contested Matrimonial / Divorce / Child Custody",
        "action": "Explain that family law matters require specialized family court advocates and mandatory court mediation. Refer to DLSA / NALSA Legal Aid helpline 15100."
    },
    {
        "domain": "High-Value Commercial Corporate Litigation (> ₹50 Lakhs)",
        "action": "Advise that dispute exceeds District Consumer Commission jurisdiction and requires Senior Advocate representation in High Court / NCLT."
    }
]

def get_domain_statutes(domain_key: str) -> Dict[str, Any]:
    return VERIFIED_STATUTES.get(domain_key, {})

def match_domain_by_text(text: str) -> str:
    """Classifies user narrative into one of the supported consumer/civil categories."""
    t = text.lower()
    
    # Check out-of-scope criminal / divorce first
    if any(k in t for k in ["kill", "murder", "assault", "beat up", "rape", "pocso", "arrest", "fir for assault", "divorce", "child custody"]):
        return "out_of_scope"
        
    # Tenancy & Rent
    if any(k in t for k in ["landlord", "security deposit", "rent deposit", "vacat", "tenant", "brokerage", "painting charges", "flat deposit", "house rent"]):
        return "tenancy_deposit"
        
    # E-Commerce & Retail
    if any(k in t for k in ["flipkart", "amazon", "myntra", "meesho", "defective", "damaged phone", "dead pixel", "replacement", "delivery", "e-commerce", "seller refused"]):
        return "ecommerce_defective_goods"
        
    # Coaching / Edtech
    if any(k in t for k in ["coaching", "edtech", "allen", "fiitjee", "byju", "batch", "tuition", "course fee", "non-refundable fee", "institute refused"]):
        return "edtech_coaching_fee"
        
    # Airline / Travel
    if any(k in t for k in ["airline", "flight", "indigo", "air india", "spicejet", "credit shell", "cancelled flight", "boarding", "ticket refund"]):
        return "airline_flight_refund"
        
    # Unpaid Salary / Freelance
    if any(k in t for k in ["unpaid salary", "freelance", "invoice", "client not paying", "stipend", "wages", "delayed payment", "contractor fee"]):
        return "unpaid_freelance_salary"
        
    # Default to e-commerce/consumer if it mentions purchase/refund/money withheld
    if any(k in t for k in ["refund", "money", "cheated", "fraud", "scam", "customer care"]):
        return "ecommerce_defective_goods"
        
    return "general_consumer"
