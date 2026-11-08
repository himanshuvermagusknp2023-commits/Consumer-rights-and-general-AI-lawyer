#!/usr/bin/env python3
"""
NyayaSetu - Core Unit & Integration Tests
Tests entity extraction, statutory grounding, anti-hallucination guardrails, and drafting.
Run with: python3 -m unittest discover tests
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nyayasetu.core.case_builder import extract_monetary_amount, detect_evidence_items, build_case_sheet
from nyayasetu.core.statutes import match_domain_by_text, VERIFIED_STATUTES
from nyayasetu.core.llm_client import LegalAIEngine
from nyayasetu.core.drafter import draft_legal_notice

class TestNyayaSetuCore(unittest.TestCase):

    def test_extract_monetary_amount(self):
        # Rupee symbol
        self.assertEqual(extract_monetary_amount("I paid ₹60,000 to the landlord."), 60000)
        # Lakh notation
        self.assertEqual(extract_monetary_amount("The coaching fee was 1.4 lakh upfront."), 140000)
        # Rs notation
        self.assertEqual(extract_monetary_amount("Flight cost was rs 19,800 only."), 19800)
        # k notation
        self.assertEqual(extract_monetary_amount("Invoice value was 45k."), 45000)

    def test_detect_evidence_items(self):
        text = "I have the signed rent agreement, upi transaction slip and whatsapp chats."
        res = detect_evidence_items(text)
        self.assertIn("Payment Proof / Bank Statement / UPI Slip", res["found"])
        self.assertIn("Written Agreement / Contract / Terms", res["found"])
        self.assertIn("Written Communication / WhatsApp / Email", res["found"])
        self.assertIn("Photographic / Video Evidence", res["missing"])

    def test_domain_classification(self):
        self.assertEqual(match_domain_by_text("Landlord kept flat security deposit painting"), "tenancy_deposit")
        self.assertEqual(match_domain_by_text("Flipkart delivered defective mobile screen green line"), "ecommerce_defective_goods")
        self.assertEqual(match_domain_by_text("IndiGo flight cancelled credit shell wallet"), "airline_flight_refund")
        self.assertEqual(match_domain_by_text("Coaching institute non-refundable fee Kota"), "edtech_coaching_fee")
        self.assertEqual(match_domain_by_text("Client startup invoice unpaid freelance dues"), "unpaid_freelance_salary")
        # Adversarial
        self.assertEqual(match_domain_by_text("Arrest neighbor murder assault FIR"), "out_of_scope")
        self.assertEqual(match_domain_by_text("Ex-parte divorce without alimony"), "out_of_scope")

    def test_safety_guardrail(self):
        engine = LegalAIEngine(model_type="deterministic")
        res = engine.process_case("My neighbor abused me and threw trash. I want IPC section to arrest him without bail.")
        self.assertEqual(res["status"], "out_of_scope")
        self.assertFalse(res["is_safe"])
        self.assertIn("112", res["message"])
        self.assertIn("15100", res["message"])
        # Ensure no legal notice was generated for illegal arrest request
        self.assertNotIn("legal_drafts", res)

    def test_draft_legal_notice_integrity(self):
        case = {
            "category": "tenancy_deposit",
            "principal_claim_amount": 50000,
            "respondent": "Mr. Sharma (Landlord)",
            "dispute_summary": "Security deposit not returned after vacating premises."
        }
        notice = draft_legal_notice(case)
        self.assertIn("LEGAL DEMAND NOTICE", notice)
        self.assertIn("INR 50,000", notice)
        self.assertIn("15 (FIFTEEN) DAYS", notice)
        self.assertIn("Transfer of Property Act", notice)
        self.assertIn("Section 108(m)", notice)

    def test_end_to_end_pipeline(self):
        engine = LegalAIEngine(model_type="deterministic")
        narrative = "I vacated my 2BHK flat in HSR Layout Bangalore on Oct 15. Landlord Ramesh withheld ₹60,000 deposit claiming 45k painting charges. I have agreement, upi slip and whatsapp chats."
        res = engine.process_case(narrative, language="hinglish")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["category"], "tenancy_deposit")
        self.assertEqual(res["case_sheet"]["principal_claim_amount"], 60000)
        self.assertIn("legal_notice", res["legal_drafts"])
        self.assertIn("consumer_petition", res["legal_drafts"])
        self.assertIn("nch_grievance", res["legal_drafts"])
        self.assertIn("whatsapp_escalation", res["legal_drafts"])
        self.assertGreaterEqual(len(res["roleplay_scenarios"]), 1)

if __name__ == "__main__":
    unittest.main()
