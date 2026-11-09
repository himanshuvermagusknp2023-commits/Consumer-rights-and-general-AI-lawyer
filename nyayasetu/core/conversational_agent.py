"""
NyayaSetu - Conversational Agent Core
Explicitly implements the 4 Task Pillars from Kuku Problem Statement 2:
1. Build the case: turn a messy story into what happened, when, and what proof they have
2. Explain where they stand and what their options are, in plain language
3. Prepare what they need, like a legal notice, a complaint, a reply or an application
4. Help them argue, for example by playing the other side so they can practise
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from .statutes import VERIFIED_STATUTES, match_domain_by_text
from .case_builder import build_case_sheet, extract_monetary_amount, detect_evidence_items

class ConversationalLegalAgent:
    def __init__(self, model_type: str = "deterministic", api_key: Optional[str] = None):
        self.model_type = model_type.lower()
        self.api_key = api_key

    def process_message(self, message: str, history: Optional[List[Dict[str, str]]] = None, session_state: Optional[Dict[str, Any]] = None, language: str = "english") -> Dict[str, Any]:
        """
        Processes an incoming user message in a multi-turn conversation.
        Updates state across the 4 Pillars.
        """
        history = history or []
        session_state = session_state or {}

        # Check for scope / emergency
        category = match_domain_by_text(message)
        if category == "out_of_scope":
            return {
                "reply": (
                    "⚠️ **MANDATORY LEGAL SAFETY NOTICE & SCOPE BOUNDARY**\n\n"
                    "This matter appears to involve potential criminal offenses, physical threats, or specialized matrimonial/divorce litigation. "
                    "NyayaSetu is strictly an everyday civil and consumer rights assistant.\n\n"
                    "**Immediate Actions Required:**\n"
                    "• **For immediate safety / police FIR:** Dial **112** (National Emergency Helpline) or visit your nearest Police Station.\n"
                    "• **For free certified advocate aid:** Call the **National Legal Services Authority (NALSA)** helpline at **15100**.\n"
                    "• **For matrimonial/custody disputes:** Consult a licensed Family Court advocate. AI cannot draft criminal petitions or divorce proceedings."
                ),
                "is_out_of_scope": True,
                "four_pillars": None
            }

        # Check if user is in Pillar 4 (Roleplay mode)
        if session_state.get("mode") == "roleplay":
            return self._handle_roleplay_interaction(message, session_state, language)

        # Normal intake: Build all 4 pillars based on the accumulated narrative
        accumulated_text = message
        for h in history:
            if h.get("role") == "user":
                accumulated_text += " " + h.get("content", "")

        four_pillars = self.generate_four_pillars(accumulated_text, language=language)

        # Formulate conversational response
        cs = four_pillars["pillar_1_build_case"]
        rx = four_pillars["pillar_2_explain_standing"]
        
        reply_lines = []
        if language == "hinglish":
            reply_lines.append(f"Maine aapka case analyze kiya hai. Yeh **{four_pillars['domain_title']}** ka mamla hai.")
            reply_lines.append(f"• **Claim Amount:** ₹{cs['what_happened']['claim_amount']:,}")
            reply_lines.append(f"• **Opposite Party:** {cs['what_happened']['respondent']}")
            reply_lines.append(f"• **Proof Readiness:** {cs['what_proof']['readiness_score']}% (Aapke paas {len(cs['what_proof']['proof_available'])} proofs hain, {len(cs['what_proof']['missing_proof'])} proofs arrange karne baaki hain).")
            reply_lines.append(f"\n**Aapka Legal Stand:** {rx['standing_summary']}")
            reply_lines.append("\nMaine right side panel pe aapke 4 pillars ready kar diye hain:")
            reply_lines.append("1. **Case Sheet** (What happened, when & proof)")
            reply_lines.append("2. **Legal Standing & Options** (Plain language rights)")
            reply_lines.append("3. **Drafts** (15-Day Legal Notice, CPA Complaint, Reply, Application)")
            reply_lines.append("4. **Practice Arguing** (Roleplay simulator opposite party ke against practice karne ke liye)")
            reply_lines.append("\nAap kis option ke saath aage badhna chahte hain? Ya phir opposite party ke arguments ke against practice karein?")
        else:
            reply_lines.append(f"I have reviewed your situation under **{four_pillars['domain_title']}**.")
            reply_lines.append(f"• **Principal Claim:** ₹{cs['what_happened']['claim_amount']:,} (+ 12% statutory interest & compensation)")
            reply_lines.append(f"• **Identified Respondent:** {cs['what_happened']['respondent']}")
            reply_lines.append(f"• **Evidentiary Readiness:** {cs['what_proof']['readiness_score']}% ({len(cs['what_proof']['proof_available'])} proofs detected, {len(cs['what_proof']['missing_proof'])} missing items recommended).")
            reply_lines.append(f"\n**Where You Stand:** {rx['standing_summary']}")
            reply_lines.append("\nI have prepared all **4 Action Pillars** for you in the side panel:")
            reply_lines.append("1. 📋 **Case Sheet**: Complete breakdown of what happened, timeline (when), and proof checklist.")
            reply_lines.append("2. ⚖️ **Standing & Options**: Your statutory rights in plain language with 3 actionable pathways.")
            reply_lines.append("3. 📄 **Prepared Documents**: Ready-to-dispatch Legal Notice, e-Daakhil Complaint, Formal Reply, and Application.")
            reply_lines.append("4. 🥊 **Argument Practice**: Live simulator where you can practice defending your claim against hostile pushbacks.")
            reply_lines.append("\nWould you like me to tailor a specific legal notice, or would you like to practice arguing against their excuses?")

        return {
            "reply": "\n".join(reply_lines),
            "is_out_of_scope": False,
            "four_pillars": four_pillars,
            "session_state": {
                "category": four_pillars["category"],
                "claim_amount": cs['what_happened']['claim_amount'],
                "mode": "case_built"
            }
        }

    def generate_four_pillars(self, narrative: str, language: str = "english") -> Dict[str, Any]:
        """
        Executes the exact 4 tasks requested in Problem Statement 2:
        - Pillar 1: Build the case (What happened, When, What proof)
        - Pillar 2: Explain where they stand & options in plain language
        - Pillar 3: Prepare what they need (Legal notice, Complaint, Reply, Application)
        - Pillar 4: Help them argue (Roleplay simulator)
        """
        category = match_domain_by_text(narrative)
        if category == "out_of_scope":
            category = "ecommerce_defective_goods"

        amount = extract_monetary_amount(narrative) or 0
        evidence_data = detect_evidence_items(narrative)
        statute_info = VERIFIED_STATUTES.get(category, {})

        # -------------------------------------------------------------
        # PILLAR 1: BUILD THE CASE (What happened, When, What proof)
        # -------------------------------------------------------------
        sentences = [s.strip() for s in re.split(r'[.\n!]+', narrative) if len(s.strip()) > 10]
        
        # Chronology (When)
        timeline = []
        date_matches = re.findall(r'\b(?:on\s+)?([A-Za-z]+ \d{1,2}(?:st|nd|rd|th)?,? \d{4}|\d{1,2}(?:st|nd|rd|th)? [A-Za-z]+|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b', narrative)
        if date_matches:
            for i, d in enumerate(date_matches[:4], 1):
                timeline.append({"step": f"Timeline Event {i}", "when": d, "detail": sentences[i-1] if i-1 < len(sentences) else "Transaction milestone"})
        else:
            timeline = [
                {"step": "Initial Agreement / Purchase", "when": "Commencement date", "detail": "Transaction initiated and payment/deposit remitted."},
                {"step": "Occurrence of Defect / Dispute", "when": "During contract term", "detail": "Issue arose, goods failed, or request to refund was raised."},
                {"step": "Notice & Rejection", "when": "Recent date", "detail": "Opposite party refused refund, issued deduction, or ceased communication."}
            ]

        # Respondent inference
        respondent = "Opposite Party / Respondent"
        low = narrative.lower()
        if "landlord" in low or "owner" in low:
            respondent = "Landlord / Property Owner"
        elif "flipkart" in low:
            respondent = "Flipkart Internet Pvt. Ltd. & Merchant"
        elif "amazon" in low:
            respondent = "Amazon Seller Services Pvt. Ltd. & Merchant"
        elif "indigo" in low:
            respondent = "InterGlobe Aviation Ltd. (IndiGo)"
        elif "coaching" in low or "institute" in low:
            respondent = "Coaching Institute / Academy"
        elif "startup" in low or "client" in low or "freelance" in low:
            respondent = "Client Entity / Employer"

        pillar_1 = {
            "what_happened": {
                "summary": sentences[0] if sentences else narrative[:140],
                "claimant_role": "Aggrieved Consumer / Tenant / Service Recipient",
                "respondent": respondent,
                "dispute_type": statute_info.get("domain", "Everyday Civil Grievance"),
                "claim_amount": amount,
                "relief_sought": f"Refund of ₹{amount:,} + 12% p.a. interest + ₹15,000 damages for mental agony"
            },
            "when_timeline": timeline,
            "what_proof": {
                "proof_available": evidence_data["found"],
                "missing_proof": evidence_data["missing"],
                "readiness_score": min(100, max(30, int((len(evidence_data['found']) / 5.0) * 100))),
                "action_items": [
                    f"Ensure you preserve '{p}' as a PDF or high-res image." for p in evidence_data["found"]
                ] + [
                    f"Recommended to collect: '{m}' before dispatching formal notice." for m in evidence_data["missing"][:2]
                ]
            }
        }

        # -------------------------------------------------------------
        # PILLAR 2: EXPLAIN WHERE THEY STAND & OPTIONS (Plain Language)
        # -------------------------------------------------------------
        statutes = statute_info.get("primary_statutes", [])
        standing_summary = (
            f"Under Indian law ({statute_info.get('domain')}), you possess a strong legal right to recover your ₹{amount:,}. "
            "The law strictly prohibits arbitrary withholding, unilateral non-refundable clauses, and unproven deductions. "
            "You are not required to hire an expensive advocate to enforce your basic consumer/tenancy rights."
        )
        if language == "hinglish":
            standing_summary = (
                f"Indian Law ({statute_info.get('domain')}) ke mutabiq aapka legal position bohot strong hai. "
                f"Opposite party ka aapka ₹{amount:,} rokna illegal hai. "
                "Koyi bhi company ya landlord unilateral 'non-refundable' ya 'painting deduction' bol kar aapka haq nahi cheen sakta."
            )

        options = [
            {
                "option_no": 1,
                "name": "Formal 15-Day Statutory Demand Notice (Pre-Litigation)",
                "summary": "Send a formal legal notice via Registered Speed Post AD & Email giving 15 days to refund principal + 12% interest.",
                "why_it_works": "Over 75% of Indian consumer/tenancy disputes settle here when the party realizes you have exact statutory citations and court readiness.",
                "cost": "₹0 to ₹50 (Speed Post)",
                "timeframe": "15 working days"
            },
            {
                "option_no": 2,
                "name": "National Consumer Helpline (NCH - 1915) / INGRAM Grievance",
                "summary": "Lodge an online complaint at consumerhelpline.gov.in or Toll-Free 1915. Government grievance officers summon the company's Nodal Officer.",
                "why_it_works": "Mandatory 30-day corporate response required under Ministry of Consumer Affairs rules.",
                "cost": "100% Free",
                "timeframe": "30 to 45 days"
            },
            {
                "option_no": 3,
                "name": "Online Consumer Commission Petition (e-Daakhil / DCDRC)",
                "summary": "File a direct petition before the District Consumer Commission under Section 35 CPA 2019. Zero court fee up to ₹5 Lakh.",
                "why_it_works": "Consumers can argue their own case without hiring a private advocate. Forum awards refund + interest + harassment compensation.",
                "cost": "₹0 (for claims under ₹5L)",
                "timeframe": "3 to 6 months"
            }
        ]

        pillar_2 = {
            "standing_summary": standing_summary,
            "statutory_anchors": [f"{s['act']} ({s['section']}): {s['title']}" for s in statutes],
            "options": options,
            "limitation_period": statute_info.get("limitation_period", "2-3 years under statutory limitation"),
            "authorities": statute_info.get("authorities", [])
        }

        # -------------------------------------------------------------
        # PILLAR 3: PREPARE WHAT THEY NEED (Notice, Complaint, Reply, Application)
        # -------------------------------------------------------------
        pillar_3 = {
            "legal_notice": self._draft_legal_notice(pillar_1, category),
            "consumer_complaint": self._draft_consumer_complaint(pillar_1, category),
            "formal_reply": self._draft_formal_reply(pillar_1, category),
            "formal_application": self._draft_application(pillar_1, category)
        }

        # -------------------------------------------------------------
        # PILLAR 4: HELP THEM ARGUE (Roleplay Simulator)
        # -------------------------------------------------------------
        pillar_4 = self._build_roleplay_scenarios(category, amount, language)

        return {
            "domain_title": statute_info.get("domain", "Everyday Civil Grievance"),
            "category": category,
            "pillar_1_build_case": pillar_1,
            "pillar_2_explain_standing": pillar_2,
            "pillar_3_prepare_documents": pillar_3,
            "pillar_4_help_them_argue": pillar_4
        }

    def _handle_roleplay_interaction(self, user_rebuttal: str, session_state: Dict[str, Any], language: str) -> Dict[str, Any]:
        """
        Handles interactive argument practice where the user replies to the opposing party's objection.
        """
        category = session_state.get("category", "tenancy_deposit")
        objection = session_state.get("current_objection", "We have a strict company policy / contract clause.")
        
        # Analyze user's rebuttal
        u_low = user_rebuttal.lower()
        has_statute = any(k in u_low for k in ["act", "section", "consumer protection", "transfer of property", "contract", "wear and tear", "gst", "invoice", "court", "lok adalat", "ccpa", "dgca"])
        has_evidence = any(k in u_low for k in ["proof", "receipt", "agreement", "chat", "email", "bill", "bank", "video"])

        feedback_points = []
        if has_statute:
            feedback_points.append("✓ Strong statutory reference: Citing specific laws immediately puts the opposing party on the defensive.")
        else:
            feedback_points.append("💡 Tip: Add the statutory section (e.g. CPA Section 2(11) or Transfer of Property Act Sec 108m) to make your argument legally binding.")

        if has_evidence:
            feedback_points.append("✓ Evidentiary backing: Mentioning existing receipts or chat records shows you have an auditable paper trail.")
        else:
            feedback_points.append("💡 Tip: Demand itemized GST invoices or mention your bank statement to shift the burden of proof.")

        if language == "hinglish":
            reply_text = (
                f"🥊 **Roleplay Evaluation (Opposing Party Defense Practice):**\n\n"
                f"**Aapka Rebuttal:** \"{user_rebuttal}\"\n\n"
                f"**Legal Coach Feedback:**\n" + "\n".join(feedback_points) + "\n\n"
                f"**Strong Recommended Polish (Hinglish):**\n"
                f"\"Aapka clause Indian law ke upar nahi ho sakta. Transfer of Property Act / Consumer Protection Act ke mutabiq arbitrary deduction void hai. Kripya 7 din mein itemized GST bill provide karein ya poora refund release karein, varna Lok Adalat / Consumer Forum mein complaint darj hogi.\""
            )
        else:
            reply_text = (
                f"🥊 **Roleplay Practice Evaluation:**\n\n"
                f"**Your Argument:** \"{user_rebuttal}\"\n\n"
                f"**Legal Coach Analysis:**\n" + "\n".join(feedback_points) + "\n\n"
                f"**Optimized Legal Rebuttal:**\n"
                f"\"Your internal terms cannot supersede statutory protections under the Consumer Protection Act / Transfer of Property Act. Unilateral deductions without verified third-party GST invoices constitute an Unfair Contract and breach of contract. Please remit the refund within 7 working days, failing which formal proceedings will be initiated before the competent Forum.\""
            )

        return {
            "reply": reply_text,
            "is_out_of_scope": False,
            "session_state": session_state
        }

    # Document Generators for Pillar 3
    def _draft_legal_notice(self, p1: Dict[str, Any], category: str) -> str:
        wh = p1["what_happened"]
        amount = wh["claim_amount"]
        respondent = wh["respondent"]
        summary = wh["summary"]
        today_str = datetime.now().strftime("%d %B, %Y")

        if category == "tenancy_deposit":
            statute_clause = (
                "Under Section 108(m) of the Transfer of Property Act, 1882 read with Model Tenancy Act principles, "
                "normal wear and tear is the landlord's obligation. Arbitrary deductions without itemized contractor GST "
                "bills constitute unjust enrichment and breach of contract under Section 70 and 73 of the Indian Contract Act, 1872."
            )
        elif category == "airline_flight_refund":
            statute_clause = (
                "Under DGCA CAR Section 3, Series M, Part IV and the Supreme Court ruling in Pravasi Legal Cell vs. UOI (2020), "
                "unilateral credit shells are illegal; passenger has the statutory right to full refund in original payment mode."
            )
        elif category == "edtech_coaching_fee":
            statute_clause = (
                "Under CCPA Coaching Guidelines 2024 and Section 2(46) CPA 2019, 'non-refundable fee' clauses are void as Unfair Contracts. "
                "Institutes are legally obligated to issue pro-rata refunds for unutilized course duration."
            )
        elif category == "unpaid_freelance_salary":
            statute_clause = (
                "Under Section 70 and 73 of the Indian Contract Act, 1872 and Section 15 of MSMED Act, failure to disburse accepted "
                "deliverables constitutes wrongful withholding attracting compound interest."
            )
        else:
            statute_clause = (
                "Under Section 2(10), 2(11), and 2(47) of the Consumer Protection Act, 2019, delivering defective goods and refusing "
                "timely refund/replacement constitutes Gross Deficiency in Service and Unfair Trade Practice."
            )

        return f"""================================================================================
FORMAL LEGAL DEMAND NOTICE (WITHOUT PREJUDICE)
SENT VIA REGISTERED SPEED POST WITH A.D. & OFFICIAL EMAIL
================================================================================
DATE: {today_str}

TO:
{respondent}
[Full Registered Office / Residential Address]
Email: [Official Grievance Email]

FROM:
[Complainant / Aggrieved Citizen Name]
[Residential Address / Contact Phone / Email]

SUBJECT: DEMAND NOTICE FOR REFUND OF INR {amount:,}/- WITH 12% ACCRUED INTEREST
AND COMPENSATION FOR DEFICIENCY IN SERVICE AND UNFAIR TRADE PRACTICE.

SIR / MADAM,

Under explicit instructions and on behalf of myself, this formal Legal Demand Notice is hereby served upon you:

1. FACTUAL BACKGROUND:
   a) That the Claimant engaged in a lawful commercial/tenancy/service agreement with you, remitting payment/deposit of INR {amount:,}/-.
   b) {summary}
   c) That despite repeated follow-ups, emails, and reminders, you have wrongfully withheld the legitimate funds due to the Claimant.

2. STATUTORY GROUNDS & VIOLATIONS:
   {statute_clause}

3. FORMAL DEMANDS (15-DAY CURE PERIOD):
   You are hereby called upon to:
   i. Immediately refund the principal amount of INR {amount:,}/- (Indian Rupees {amount:,} only) into the Claimant's designated bank account within 15 (FIFTEEN) DAYS of the receipt of this Notice;
   ii. Pay statutory interest at 12% per annum from the date the amount became due until the date of realization;
   iii. Pay an amount of INR 15,000/- towards damages for mental harassment and costs incurred in issuing this formal notice.

TAKE NOTICE that failure to comply within 15 days will constrain the Claimant to initiate formal legal proceedings before the Competent District Consumer Disputes Redressal Commission / Civil Court, holding you liable for all legal expenses, punitive damages, and interest.

Yours faithfully,

_____________________________
[Complainant / Authorized Signatory]
Enclosures: Bank Transaction Proof, Agreement Copy, Communication Records.
================================================================================"""

    def _draft_consumer_complaint(self, p1: Dict[str, Any], category: str) -> str:
        wh = p1["what_happened"]
        amount = wh["claim_amount"]
        respondent = wh["respondent"]
        summary = wh["summary"]

        return f"""BEFORE THE HON'BLE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION
AT: [DISTRICT NAME, STATE]

CONSUMER COMPLAINT NO. ________ / {datetime.now().year}
(Under Section 35 of the Consumer Protection Act, 2019)

IN THE MATTER OF:
[Complainant Name]
Residing at: [Address & Contact Details]                ... COMPLAINANT

VERSUS

{respondent}
Having Office at: [Registered Address]                 ... OPPOSITE PARTY

MEMORANDUM OF COMPLAINT UNDER SECTION 35 OF CPA 2019

1. JURISDICTION:
   The Complainant is a 'Consumer' under Section 2(7) of CPA 2019. The total claim value (INR {amount:,}/-) is under INR 50,00,000/-, conferring complete pecuniary and territorial jurisdiction on this Hon'ble Commission.

2. FACTS OF THE CASE:
   a) Consideration of INR {amount:,}/- was duly paid to the Opposite Party.
   b) {summary}
   c) A formal 15-day Demand Notice dated [Notice Date] was served, but Opposite Party failed to remediate the grievance.

3. DEFICIENCY IN SERVICE & UNFAIR TRADE PRACTICE:
   The Opposite Party's actions violate Section 2(11) (Deficiency in Service) and Section 2(47) (Unfair Trade Practice) of the Act.

4. PRAYER / RELIEFS:
   The Complainant prays for:
   a) Full refund of INR {amount:,}/- with 12% interest p.a.;
   b) Compensation of INR 25,000/- for mental agony and harassment;
   c) Litigation expenses of INR 10,000/-.

VERIFICATION:
I verify that the contents of paragraphs 1 to 4 are true to my personal knowledge.
DEPONENT (Complainant in Person)
"""

    def _draft_formal_reply(self, p1: Dict[str, Any], category: str) -> str:
        wh = p1["what_happened"]
        amount = wh["claim_amount"]
        respondent = wh["respondent"]

        return f"""FORMAL REPLY TO DEDUCTION / REJECTION NOTICE
--------------------------------------------------------------------------------
DATE: {datetime.now().strftime("%d %B, %Y")}
TO: {respondent}
RE: Rebuttal against deduction / refund rejection notice for INR {amount:,}/-

Dear Sir/Madam,

I am in receipt of your communication regarding the deduction/refusal of my refund of INR {amount:,}/-.

Please be advised that your stated grounds are legally untenable:
1. Under Indian law (Transfer of Property Act Sec 108(m) / Consumer Protection Act 2019 Sec 2(46)), standard boilerplate clauses and arbitrary deductions without verified third-party contractor tax invoices are legally void as unfair terms.
2. In the absence of documented mutual inspection reports and verifiable GST invoices, any unilateral withholding constitutes unauthorized retention and unjust enrichment.

I reiterate my formal demand for the immediate release of INR {amount:,}/- within 7 days, failing which this matter will be escalated to the National Consumer Helpline (1915) and the competent District Consumer Commission without further notice.

Sincerely,
[Complainant Name]
"""

    def _draft_application(self, p1: Dict[str, Any], category: str) -> str:
        wh = p1["what_happened"]
        amount = wh["claim_amount"]
        respondent = wh["respondent"]

        return f"""APPLICATION FOR GRIEVANCE REDRESSAL & IMMEDIATE REFUND
--------------------------------------------------------------------------------
SUBMITTED TO: Grievance Redressal Officer / Nodal Authority, {respondent}
CC: National Consumer Helpline (INGRAM Portal - 1915)

1. APPLICANT DETAILS:
   Name: [Complainant Name] | Mobile: [Phone] | Email: [Email]

2. TRANSACTION IDENTIFIERS:
   Reference / Order / Agreement ID : [ID Number]
   Disputed Consideration           : INR {amount:,}/-
   Date of Transaction              : [Transaction Date]

3. STATEMENT OF GRIEVANCE:
   The applicant availed services/goods in good faith. Due to failure in performance / refusal of legitimate return, the amount of INR {amount:,}/- remains wrongfully retained by the entity.

4. RELIEF SOUGHT:
   Order an immediate refund of INR {amount:,}/- to the applicant's source bank account within 48 hours in compliance with statutory consumer guidelines.

Applicant Signature: _______________________
"""

    def _build_roleplay_scenarios(self, category: str, amount: int, language: str) -> List[Dict[str, Any]]:
        from .simulator import get_roleplay_scenarios
        base = get_roleplay_scenarios(category)
        scenarios = []
        for b in base:
            scenarios.append({
                "objection": b["objection"],
                "intent": b["intent"],
                "statutory_anchor": b["statutory_anchor"],
                "suggested_rebuttal": b["rebuttal_hinglish"] if language == "hinglish" else b["rebuttal_english"]
            })
        return scenarios

