# NyayaSetu (न्याय सेतु): Conversational AI Legal Navigator for Indian Everyday Rights
**Kuku AI Generalist Assignment — Problem Statement 2: Build an AI Lawyer**  
*Deliverable:* 2-Page Executive Solution Document

---

## 1. Problem Choice, Framing & Scope
In India, an estimated **95% of everyday civil grievances**—unreturned rental security deposits (₹30,000–₹1,50,000), e-commerce refusal to refund defective goods (₹2,000–₹50,000), cancelled flight credit shells, coaching institute fee forfeitures, and delayed freelance invoices—never reach legal redress.

**The Economic Paradox:** Retaining a civil advocate requires ₹20,000 to ₹50,000 upfront. For claims under ₹1–2 Lakhs, legal action is economically irrational ("the remedy costs more than the loss"). Furthermore, complex terminology (*Section 108 Transfer of Property Act, Section 35 CPA 2019, Deficiency in Service*) intimidates citizens into silence.

**Scoping Strategy:** Rather than an "all-law generalist" that fails across 1,200 Indian statutes, **NyayaSetu specializes strictly in Consumer & Everyday Civil Rights**. Over 75% of these disputes resolve in pre-litigation once the opposing party realizes the citizen possesses verified statutory citations, an evidentiary chronology, and a formal legal demand notice.

---

## 2. The 4 Task Pillars Implemented

NyayaSetu directly addresses the 4 core tasks specified in the assignment brief:

### Pillar 1: Build the Case (What Happened, When, and What Proof)
* **What Happened:** Conversational intake extracts claimant, respondent, dispute facts, and monetary exposure.
* **When (Timeline):** Chronologically orders events from initial contract to defect occurrence, follow-ups, and rejection.
* **What Proof (Evidentiary Health Meter):** Audits available proof (UPI receipts, agreements, WhatsApp chats, unboxing videos) and calculates an **Evidentiary Readiness Score (0-100%)**, flagging missing documents needed before formal notice.

### Pillar 2: Explain Where They Stand & Options in Plain Language
* **Legal Standing:** Plain-English & conversational Hinglish breakdown of statutory rights under the *Consumer Protection Act 2019*, *Transfer of Property Act 1882*, and *Model Tenancy Act*.
* **Actionable 3-Tier Options:** 
  1. *Tier 1: 15-Day Statutory Demand Notice* (pre-litigation cure period).
  2. *Tier 2: National Consumer Helpline (NCH 1915 / INGRAM)* (free government-mediated conciliation).
  3. *Tier 3: Online e-Daakhil / District Consumer Commission (DCDRC)* (zero court fee under ₹5 Lakh, no private lawyer required).

### Pillar 3: Prepare What They Need (Actionable Legal Artifacts)
* Generates four complete, ready-to-dispatch legal documents:
  1. **Formal Legal Notice:** Standard 15-day Demand Notice with statutory citations.
  2. **Formal Consumer Complaint:** Memorandum of Complaint under Section 35 CPA 2019 for e-Daakhil.
  3. **Formal Rebuttal Reply:** Rebuts landlord deduction notices or corporate refusal emails.
  4. **Refund Application:** Formatted for company Nodal Officers and the National Consumer Helpline.

### Pillar 4: Help Them Argue (Interactive Roleplay Simulator)
* Equips citizens with counter-arguments to defeat intimidating pushbacks from landlords and corporations (e.g. *"Clause 14 says 1 month rent is deducted for painting automatically"* ➔ *Rebuttal: Section 108(m) TPA makes wear & tear owner's liability; arbitrary deductions without contractor GST invoices are void under Section 23 Contract Act*).
* Features an **Interactive Rehearsal Box** where users submit arguments and receive real-time coaching feedback.

---

## 3. Approach & Architecture: AI vs. Deterministic Rules
* **What We Delegated to AI:** Multilingual conversational intake (Web Speech API supporting Hindi/English voice input), messy narrative structuring, entity extraction, and simulating the adversary's counter-arguments.
* **What We Kept as Deterministic Rules:** Statutory sections, limitation periods, court fees, and template formatting. The model is **structurally prohibited from generating free-form penal sections or case citations**.
* **Pluggable Model Architecture:** Abstract engine interface (`LegalAIEngine`) allows 1-click swapping between the *Local Deterministic Rule Engine (0s latency, 100% offline, $0 cost, 0% hallucination)*, *Google Gemini Flash*, or *OpenAI GPT-4o-mini*.

---

## 4. Human-in-the-Loop & Safety Guardrails
* **Non-Waivable Scope Boundary:** If a user prompts criminal offenses, physical threats, matrimonial divorce, or claims > ₹50 Lakhs, drafting halts and the citizen is routed to **Dial 112 (Police)** or **NALSA 15100** for certified legal aid.
* **Transparent Non-Advocate Disclaimer:** Explicit notice that NyayaSetu provides self-help legal dispute assistance, not an advocate-client relationship.

---

## 5. Economics, Latency & Scale to 1.4 Billion People
* **Unit Economics at Volume:** With Gemini Flash or deterministic processing, processing 10,000 cases costs **under $3.00 total** (~800 prompt tokens, ~1,200 output tokens per case).
* **Mass Indian Deployment Strategy:** Can be ported in 48 hours to a WhatsApp Business chatbot via Meta Cloud API, integrated with **Bhashini** (Govt of India AI translation) for 22 scheduled Indian languages, directly feeding into the National Consumer Helpline (NCH - 1915) API.

---

## 6. Evaluation, Quality Checking & Benchmark Runs
Evaluated across 6 real-world benchmark test cases (`nyayasetu/test_cases/`):

| ID | Dispute Scenario | Claim | Grounded Indian Statutes | Readiness | Anti-Hallucination Audit |
|---|---|---|---|---|---|
| **CASE-01** | Tenant Deposit Retention (Painting) | ₹60,000 | TPA Sec 108(m), Model Tenancy Act, Contract Act Sec 73 | 100% | PASS (0 fake acts) |
| **CASE-02** | Flipkart Defective Phone (7-day loop) | ₹48,000 | CPA 2019 Sec 2(10), 2(11), 2(47), E-Com Rules 2020 | 60% | PASS (0 fake acts) |
| **CASE-03** | IndiGo Cancelled Flight Credit Shell | ₹19,800 | DGCA CAR Series M Part IV, Pravasi Legal (SC) | 80% | PASS (0 fake acts) |
| **CASE-04** | Coaching Institute Advance Fee Lock | ₹1,40,000 | CPA 2019 Sec 2(46), CCPA Coaching Rules 2024 | 40% | PASS (0 fake acts) |
| **CASE-05** | Startup Freelancer Unpaid Invoice | ₹45,000 | Contract Act Sec 70 & 73, MSMED Act Sec 15 & 16 | 80% | PASS (0 fake acts) |
| **CASE-06** | Adversarial Scope: Arrest Neighbor | Civic / N/A | None (Refused criminal arrest / divorce scope) | N/A | PASS (Blocked & Routed to 112) |

---

## 7. Honest Limitations & Where the System Fails
1. **User Factual Misrepresentation:** If a tenant concealed deliberate property destruction or a consumer tampered with an electronic device, the AI assumes good faith. The generated notice will collapse under cross-examination if the respondent produces counter-evidence.
2. **State-Level Rent Control Nuances:** While the Consumer Protection Act 2019 is uniform across India, tenancy statutes vary by state (e.g. Karnataka Rent Act vs. Maharashtra Rent Control Act). NyayaSetu anchors on the national Transfer of Property Act and Model Tenancy Act, but state-specific deposit registry procedures still require localized lawyer oversight.
3. **High-Conflict or Disputed Oral Evidence:** For complex claims involving oral promises, fraud allegations, or high financial stakes, automated notices cannot substitute for formal evidentiary discovery and cross-examination by an advocate.
