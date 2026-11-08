# NyayaSetu (न्याय सेतु): AI Legal Navigator for Indian Consumer & Everyday Rights
**Kuku AI Generalist Assignment — Problem Statement 2: Build an AI Lawyer**  
*Author:* AI Generalist Candidate | *Date:* November 2024 | *Deliverable:* 2-Page Executive Brief

---

## 1. Problem Choice, Framing & Scope
In India, an estimated **95% of everyday civil grievances**—unreturned rental deposits (₹30,000–₹1,50,000), e-commerce refusal to refund defective goods (₹2,000–₹50,000), cancelled flight credit shells, coaching institute fee forfeitures, and delayed freelance invoices—never see legal redress. 

**The Economic Paradox:** Retaining an advocate for a civil recovery suit costs ₹20,000 to ₹50,000 upfront. For claims under ₹1–2 Lakhs, the dispute is economically irrational to litigate ("the cure costs more than the disease"). Furthermore, legal terminology (*Section 108 Transfer of Property Act, Section 35 CPA 2019, Deficiency in Service*) intimidates ordinary citizens into abandoning valid claims.

**The Strategic Scope:** Rather than building an "all-law generalist" that fails across 1,200 Indian statutes, **NyayaSetu specializes strictly in Consumer & Everyday Civil Rights**. Over 75% of these disputes resolve in pre-litigation once the opposing party realizes the claimant possesses verified statutory citations, an evidentiary chronology, and a ready-to-file legal notice.

---

## 2. Approach & Architecture: AI vs. Deterministic Rules
To eliminate hallucinations while preserving conversational empathy, NyayaSetu implements a **hybrid neuro-symbolic pipeline**:

```
[Raw Narrative (Voice/Text/Hinglish)]
                 │
                 ▼
    ┌──────────────────────────┐
    │ Conversational Extractor │ ➔ Extracts: Amounts, Parties, Dates, Evidentiary Artifacts
    └────────────┬─────────────┘
                 ▼
    ┌──────────────────────────┐
    │ Deterministic Knowledge  │ ➔ Verified Statutory Grounding (CPA 2019, Model Tenancy Act,
    │ & Safety Rules Engine    │   DGCA CAR, Contract Act 1872). ZERO LLM Law Fabrication.
    └────────────┬─────────────┘
                 ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │ Multi-Modal Action Engine                                              │
    │  ├─ 1. Evidentiary Readiness Audit (Found vs Missing Proof Checklist)   │
    │  ├─ 2. Plain Language & Hinglish Standing Explainer                    │
    │  ├─ 3. Drafting Studio (15-Day Demand Notice, e-Daakhil DCDRC, NCH)   │
    │  └─ 4. "Devil's Advocate" Roleplay Rebuttal Simulator                  │
    └────────────────────────────────────────────────────────────────────────┘
```

* **What We Delegate to AI:** Conversational intake of messy emotional narratives, voice transcription (Web Speech API supporting Hindi/English), entity extraction, and simulating the opposing party's negotiation pushbacks.
* **What We Hardcode as Deterministic Rules:** Legal sections, limitation periods, court fees, and template structures. The model is **strictly prohibited from generating free-form penal sections or case citations**.
* **Pluggable Model Architecture:** Built with an abstract provider interface (`LegalAIEngine`). Ships with a zero-dependency deterministic engine (0s latency, 100% offline, $0 cost) and swappable 1-click connectors for Google Gemini Flash and OpenAI GPT-4o-mini.

---

## 3. Human-in-the-Loop & Safety Guardrails
1. **Evidentiary Readiness Meter:** Before generating a demand notice, the system audits the user's proof (e.g., bank UPI slips, agreement, WhatsApp chats, unboxing videos). If proof is missing, it flags specific items required to prevent premature escalation.
2. **Strict Scope Guardrail & Advocate Referral:** Non-waivable safety filter. If the narrative detects criminal offenses, physical threats, matrimonial disputes, or claims > ₹50 Lakhs, the system halts generation and directs the citizen to **Dial 112 (Police)** or **15100 (National Legal Services Authority - NALSA)** for certified advocate assistance.
3. **Transparent Non-Advocate Disclaimer:** Explicit notice that NyayaSetu provides legal information and self-help dispute documentation under Indian law, not formal advocate representation.

---

## 4. Economics, Latency & Real-World Scale
* **Inference Cost at Volume:** With Gemini Flash or local deterministic processing, processing 10,000 cases costs **under $3.00 total** (~800 prompt tokens, ~1,200 output tokens per case). 
* **Zero Dependency Web Runtime:** The prototype runs on pure Python 3 standard library (`http.server`, `urllib`, `json`). Zero `pip install` compilation issues or external server requirements.
* **Mass Indian Deployment Strategy:** Can be ported in 48 hours to a WhatsApp Business chatbot via Twilio/Meta Cloud API, integrated with **Bhashini** (Govt of India AI translation) for 22 scheduled Indian languages, directly feeding into the National Consumer Helpline (NCH - 1915) API.

---

## 5. Evaluation, Quality Checking & Benchmark Results
We evaluated NyayaSetu against 6 real-world benchmark test cases (`nyayasetu/test_cases/`):

| Test Case | Domain | Claim Value | Identified Laws | Anti-Hallucination Audit | Readiness Score |
|---|---|---|---|---|---|
| **Case 1** | Landlord Deposit Retention (Painting Excuse) | ₹60,000 | TPA Sec 108(m), Model Tenancy Act, Contract Act Sec 73 | PASS (0 fake citations) | 100% (Lease, UPI, Video) |
| **Case 2** | Flipkart Defective Phone (7-Day Loop) | ₹48,000 | CPA 2019 Sec 2(10), 2(11), 2(47), E-Com Rules 2020 | PASS (0 fake citations) | 60% (Invoice, Video) |
| **Case 3** | IndiGo Flight Cancelled (Credit Shell) | ₹19,800 | DGCA CAR Series M Part IV, Pravasi Legal Cell (SC) | PASS (0 fake citations) | 80% (PNR, Bank Slip) |
| **Case 4** | Coaching Fee Non-Refundable Clause | ₹1,40,000 | CPA 2019 Sec 2(46), CCPA Coaching Guidelines 2024 | PASS (0 fake citations) | 40% (Fee Receipt only) |
| **Case 5** | Startup Unpaid Contractor Invoice | ₹45,000 | Contract Act Sec 70 & 73, MSMED Act Sec 15 & 16 | PASS (0 fake citations) | 80% (Contract, Slack, Invoice)|
| **Case 6** | Adversarial: Arrest Neighbor for Garbage | Out of Scope | None (Refused criminal arrest / divorce scope) | PASS (Blocked & Routed to 112) | N/A (Safety Triggered) |

---

## 6. Honest Limitations & Where the System Fails
1. **User Factual Misrepresentation:** If a user conceals tenant-caused physical destruction (e.g., broken tiles) or deliberate product tampering, the generated demand notice will be factually vulnerable if challenged in court.
2. **Regional & State-Level Rent Law Nuances:** While the Consumer Protection Act 2019 is central and uniform across India, residential rent control laws vary across states (e.g., Karnataka Rent Act vs. Maharashtra Rent Control Act). NyayaSetu uses universal Transfer of Property Act and Model Tenancy Act principles, but state-specific judicial deposit registry procedures still require localized guidance.
3. **Contested Evidence & High-Stakes Litigation:** When disputes cross into disputed oral agreements, fraud allegations, or high financial damages, paper notices fail and judicial cross-examination by an advocate is indispensable.

---

## 7. Prototype Quickstart
* **Run Benchmark Evaluation:** `python3 nyayasetu/run_eval.py`
* **Launch Interactive Web App:** `python3 run_app.py 8080` (open `http://localhost:8080`)
* **Inspection of Unedited Raw Outputs:** All JSON case sheets and TXT legal notices are stored in `nyayasetu/raw_outputs/`.
