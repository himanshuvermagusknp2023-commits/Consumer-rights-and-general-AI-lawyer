# NyayaSetu — 3-Minute Video Walkthrough Script
**For Loom / Unlisted YouTube / Google Drive Submission**

---

### **[0:00 - 0:30] Introduction & Problem Framing**
> *"Hi everyone, I’m [Your Name], and this is NyayaSetu (न्याय सेतु), an AI Legal Navigator built for Problem Statement 2 of the Kuku AI Generalist Assignment.*
>
> *I chose to scope this specifically to **Indian Consumer and Everyday Civil Rights**—such as landlords refusing to return security deposits, e-commerce platforms denying refunds for defective goods, coaching centers locking advance fees, and cancelled flights forced into credit shells.*
> *In India, over 95% of these cases never reach an advocate because legal consultation costs ₹20,000 to ₹50,000 upfront. For a ₹40,000 deposit, hiring a lawyer makes no economic sense. But 75% of these disputes can be resolved in pre-litigation if the consumer knows their exact statutory rights and sends a formal demand notice."*

---

### **[0:30 - 1:15] Demo: Conversational Intake & Case Sheet Builder**
> *(Screen shows `http://localhost:8080`)*
>
> *"Let’s look at the live prototype. It runs on pure Python with zero install dependencies, and supports voice input in both Hindi and English.*
> *I’ll click our benchmark scenario: **Landlord Ramesh withholding a ₹60,000 deposit in Bengaluru claiming painting charges**.*
> *When I click 'Build Case', NyayaSetu immediately extracts:*
> 1. *The principal claim of ₹60,000 + 12% statutory interest;*
> 2. *An **Evidentiary Readiness Score** of 100%, auditing what proof the user has—like the rent agreement, UPI transaction slips, and handover video—and warning them about missing items before they send anything.*
> 3. *A plain-language breakdown in English or Hinglish showing that under **Section 108(m) of the Transfer of Property Act** and the **Model Tenancy Act**, normal wear and tear is the landlord’s liability, and arbitrary deductions without GST invoices are illegal."*

---

### **[1:15 - 2:05] Demo: Actionable Legal Drafting & 'Devil's Advocate' Simulator**
> *"Next is the **Drafting Studio**. In one click, it generates:*
> - *A formal **15-Day Legal Demand Notice** with exact statutory grounds and cure period;*
> - *A complete **District Consumer Commission (DCDRC)** petition for e-Daakhil with zero court fees under ₹5 Lakhs;*
> - *And ready-to-paste grievance text for the **National Consumer Helpline (NCH 1915)** and WhatsApp.*
>
> *Now, here is the feature I’m most excited about: **The 'Devil's Advocate' Rehearsal Simulator**. Ordinary citizens freeze when a landlord yells, 'Clause 14 gives me the right to paint, go ahead and sue me, court will take 10 years!'.*
> *NyayaSetu simulates that exact objection and equips the user with a bulletproof rebuttal: explaining that unconscionable clauses are void under Section 23 of the Contract Act, and that they can settle for free in the District Lok Adalat with zero lawyer fees."*

---

### **[2:05 - 2:40] Anti-Hallucination Guardrails & Scope Boundaries**
> *"A critical requirement in Kuku’s brief is that AI models love to hallucinate fake sections and non-existent court cases. How did I solve that?*
> 1. *NyayaSetu uses a **neuro-symbolic design**: the LLM handles conversational intake and entity extraction, but all statutory citations are strictly anchored to a verified deterministic database. The model is physically prohibited from generating free-form penal sections.*
> 2. *Let's test an adversarial input: asking to arrest a neighbor for dumping garbage. NyayaSetu immediately halts drafting, enforces the **Scope Guardrail**, and routes the user to **Dial 112** for emergency police or **NALSA 15100** for certified legal aid.*
> 3. *The model is completely pluggable: it runs instantly offline with our rule engine, or connects via API to Gemini Flash or GPT-4o-mini."*

---

### **[2:40 - 3:00] Real-World Scale & Conclusion**
> *"At scale, processing 10,000 cases costs under $3 on Gemini Flash. The entire engine can be plugged into a WhatsApp Business bot with Bhashini for 22 Indian languages.*
> *All raw outputs and the 2-page PDF solution doc are in the repository. Thank you for your time, and I look forward to running this on your test inputs during the interview!"*
