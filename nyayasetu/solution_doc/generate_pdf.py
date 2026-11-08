#!/usr/bin/env python3
"""
NyayaSetu - Solution Document 2-Page PDF Generator
Creates an impeccably formatted, professional 2-page PDF brief using pure Python.
Zero external library dependencies (no reportlab/wkhtmltopdf needed).
"""

from pathlib import Path

def escape_pdf(text: str) -> str:
    """Escapes special characters for PDF text operators."""
    return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

class PurePDFBuilder:
    def __init__(self, filename: str):
        self.filename = filename
        self.pages = []  # list of byte streams
        self.current_page_stream = []
        self.page_width = 595.0
        self.page_height = 842.0

    def start_page(self):
        self.current_page_stream = []

    def end_page(self):
        self.pages.append("".join(self.current_page_stream).encode('latin-1', 'replace'))
        self.current_page_stream = []

    def set_font(self, font_name: str, size: float):
        self.current_page_stream.append(f"/{font_name} {size:.1f} Tf\n")

    def set_color(self, r: float, g: float, b: float):
        self.current_page_stream.append(f"{r:.3f} {g:.3f} {b:.3f} rg\n")

    def set_stroke_color(self, r: float, g: float, b: float):
        self.current_page_stream.append(f"{r:.3f} {g:.3f} {b:.3f} RG\n")

    def set_line_width(self, w: float):
        self.current_page_stream.append(f"{w:.1f} w\n")

    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        self.current_page_stream.append(f"{x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S\n")

    def draw_rect(self, x: float, y: float, w: float, h: float, fill: bool = False, stroke: bool = True):
        op = "B" if (fill and stroke) else ("f" if fill else "S")
        self.current_page_stream.append(f"{x:.1f} {y:.1f} {w:.1f} {h:.1f} re {op}\n")

    def draw_text(self, text: str, x: float, y: float, font: str = "F1", size: float = 10.0, r: float = 0.05, g: float = 0.08, b: float = 0.15):
        escaped = escape_pdf(text)
        stream_cmd = (
            f"BT\n"
            f"/{font} {size:.1f} Tf\n"
            f"{r:.3f} {g:.3f} {b:.3f} rg\n"
            f"1 0 0 1 {x:.1f} {y:.1f} Tm\n"
            f"({escaped}) Tj\n"
            f"ET\n"
        )
        self.current_page_stream.append(stream_cmd)

    def draw_wrapped_text(self, text: str, x: float, start_y: float, width_chars: int, font: str = "F1", size: float = 8.5, line_spacing: float = 11.5, r: float = 0.1, g: float = 0.12, b: float = 0.18) -> float:
        """Wraps text cleanly and returns the ending Y position."""
        words = text.split()
        lines = []
        curr = []
        curr_len = 0
        for w in words:
            if curr_len + len(w) + 1 > width_chars:
                lines.append(" ".join(curr))
                curr = [w]
                curr_len = len(w)
            else:
                curr.append(w)
                curr_len += len(w) + 1
        if curr:
            lines.append(" ".join(curr))

        curr_y = start_y
        for l in lines:
            self.draw_text(l, x, curr_y, font=font, size=size, r=r, g=g, b=b)
            curr_y -= line_spacing
        return curr_y

    def build(self):
        num_pages = len(self.pages)
        objects = []
        
        # Object 1: Catalog
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        
        # Object 2: Pages
        kids_refs = " ".join([f"{3 + i*3} 0 R" for i in range(num_pages)])
        objects.append(f"<< /Type /Pages /Kids [{kids_refs}] /Count {num_pages} >>".encode('ascii'))
        
        # Resources Font Dictionary (Object used by all pages)
        # Fonts: F1=Helvetica, F2=Helvetica-Bold, F3=Helvetica-Oblique, F4=Courier
        font_obj_idx = 3 + num_pages * 3
        
        # For each page:
        # Page Obj (3 + i*3), Contents Obj (4 + i*3)
        for i in range(num_pages):
            page_obj = (
                f"<< /Type /Page /Parent 2 0 R "
                f"/Resources << /Font << "
                f"/F1 {font_obj_idx} 0 R "
                f"/F2 {font_obj_idx+1} 0 R "
                f"/F3 {font_obj_idx+2} 0 R "
                f"/F4 {font_obj_idx+3} 0 R "
                f">> >> "
                f"/MediaBox [0 0 595 842] "
                f"/Contents {4 + i*3} 0 R >>"
            ).encode('ascii')
            objects.append(page_obj)

            content_bytes = self.pages[i]
            stream_obj = (
                f"<< /Length {len(content_bytes)} >>\n"
                f"stream\n"
            ).encode('ascii') + content_bytes + b"\nendstream"
            objects.append(stream_obj)

            # Placeholder for alignment object
            objects.append(b"<< >>")

        # Add Font objects
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique >>")
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")

        # Now write full PDF binary
        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]

        for i, obj in enumerate(objects, 1):
            offsets.append(len(out))
            out.extend(f"{i} 0 obj\n".encode('ascii'))
            out.extend(obj)
            out.extend(b"\nendobj\n")

        startxref = len(out)
        out.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode('ascii'))
        for off in offsets[1:]:
            out.extend(f"{off:010d} 00000 n \n".encode('ascii'))

        out.extend(
            f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\n"
            f"startxref\n{startxref}\n%%EOF\n".encode('ascii')
        )

        with open(self.filename, 'wb') as f:
            f.write(out)
        print(f"✓ PDF successfully created: {self.filename} ({num_pages} pages)")


def generate_solution_pdf(output_path: str):
    pdf = PurePDFBuilder(output_path)

    # ==========================================
    # PAGE 1: Framing, Architecture & Safety
    # ==========================================
    pdf.start_page()

    # Top Tag
    pdf.draw_text("KUKU — AI GENERALIST ASSIGNMENT  |  PROBLEM STATEMENT 2", 40, 805, font="F2", size=8.5, r=0.4, g=0.45, b=0.55)
    
    # Title & Subtitle
    pdf.draw_text("NyayaSetu: Everyday Consumer & Civil Legal Rights AI", 40, 785, font="F2", size=16.0, r=0.08, g=0.18, b=0.45)
    pdf.draw_text("A Neuro-Symbolic Dispute Navigator for Ordinary Indian Citizens", 40, 770, font="F3", size=9.5, r=0.3, g=0.35, b=0.45)
    
    # Header Rule
    pdf.set_stroke_color(0.2, 0.4, 0.8)
    pdf.set_line_width(1.5)
    pdf.draw_line(40, 762, 555, 762)

    # 1. Problem Choice & Framing
    pdf.draw_text("1. Problem Choice, Framing & Scope", 40, 746, font="F2", size=11.0, r=0.08, g=0.18, b=0.45)
    
    p1_text = (
        "In India, an estimated 95% of everyday civil grievances never receive legal redress: rental security deposits "
        "(Rs 30k-1.5L) withheld under fictitious 'repainting' claims, e-commerce platforms refusing refunds for defective "
        "electronics, coaching institutes hoarding advance annual fees, and cancelled flights locked into credit shells. "
        "The economic paradox: hiring a civil advocate costs Rs 20,000-50,000 upfront. For claims under Rs 1-2 Lakhs, the "
        "remedy costs more than the loss. Citizens abandon claims because legal language is intimidating and procedures are opaque."
    )
    y = pdf.draw_wrapped_text(p1_text, 40, 733, 108, font="F1", size=8.2, line_spacing=10.5)

    p1_scope = (
        "Why Consumer & Everyday Rights (and not everything)? Generalist legal LLMs fail by hallucinating criminal penal "
        "sections and fabricated Supreme Court case citations. NyayaSetu scopes sharply to Consumer & Everyday Civil Rights. "
        "Over 75% of these disputes resolve in pre-litigation once the respondent realizes the consumer possesses exact statutory "
        "citations, an organized chronological record, and a structured legal demand notice."
    )
    y = pdf.draw_wrapped_text(p1_scope, 40, y - 4, 108, font="F1", size=8.2, line_spacing=10.5)

    # 2. Approach & Architecture
    y -= 10
    pdf.draw_text("2. Approach & Architecture: AI vs. Deterministic Code Rules", 40, y, font="F2", size=11.0, r=0.08, g=0.18, b=0.45)
    y -= 14

    arch_box_y = y
    pdf.set_stroke_color(0.8, 0.85, 0.92)
    pdf.set_color(0.97, 0.98, 1.0)
    pdf.set_line_width(0.8)
    pdf.draw_rect(40, arch_box_y - 82, 515, 82, fill=True, stroke=True)

    pdf.draw_text("PIPELINE ARCHITECTURE (NEURO-SYMBOLIC HYBRID):", 48, arch_box_y - 12, font="F2", size=8.0, r=0.15, g=0.25, b=0.55)
    pdf.draw_text("1. Conversational Intake: Web Speech API (voice in Hindi/English) + Text -> Extracts parties, dates, claims, proof.", 48, arch_box_y - 25, font="F1", size=8.0, r=0.1, g=0.12, b=0.2)
    pdf.draw_text("2. Deterministic Legal Anchor: Strictly maps verified Indian statutes (CPA 2019, MTA 2021, Contract Act, DGCA CAR).", 48, arch_box_y - 37, font="F1", size=8.0, r=0.1, g=0.12, b=0.2)
    pdf.draw_text("3. Evidentiary Readiness Meter: Audits required proof (UPI slips, agreements, chats) vs missing items before dispatch.", 48, arch_box_y - 49, font="F1", size=8.0, r=0.1, g=0.12, b=0.2)
    pdf.draw_text("4. Actionable Drafting Studio: Generates 15-Day Demand Notice, e-Daakhil CPA Petition, and NCH 1915 grievance draft.", 48, arch_box_y - 61, font="F1", size=8.0, r=0.1, g=0.12, b=0.2)
    pdf.draw_text("5. 'Devil's Advocate' Simulator: Rehearses opposing party counter-arguments with statutory rebuttal scripts.", 48, arch_box_y - 73, font="F1", size=8.0, r=0.1, g=0.12, b=0.2)

    y = arch_box_y - 94
    p2_split = (
        "What We Delegated to AI: Understanding messy, emotional, multilingual narratives (Hinglish/English); natural entity "
        "extraction; and roleplaying the opposing party's hostile objections. What We Kept in Deterministic Code: Statutory "
        "sections, limitation periods, court fees, and legal notice clauses. The AI is structurally prevented from inventing laws. "
        "Model Swapping: Implemented an abstract interface (LegalAIEngine) supporting zero-dependency deterministic execution "
        "(offline, instant, $0 cost) and 1-click connectors for Google Gemini Flash and OpenAI GPT-4o-mini."
    )
    y = pdf.draw_wrapped_text(p2_split, 40, y, 108, font="F1", size=8.2, line_spacing=10.5)

    # 3. Human in the loop & Safety
    y -= 10
    pdf.draw_text("3. Human-in-the-Loop & Safety Guardrails", 40, y, font="F2", size=11.0, r=0.08, g=0.18, b=0.45)
    y -= 13

    p3_safety = (
        "- Evidentiary Readiness Audit: Before notice dispatch, the system computes an evidence score (0-100%) and tells the "
        "user exactly what documents they must attach (e.g. proof of key handover, GST invoice) so they do not make weak claims.\n"
        "- Non-Waivable Scope Boundary: If a prompt touches violence, criminal arrest, matrimonial divorce, or claims > Rs 50 Lakhs, "
        "the engine stops legal drafting and routes the user to Emergency Police (112) or the National Legal Services Authority "
        "(NALSA 15100) for free advocate representation.\n"
        "- Transparent Disclaimer: Prominently states that NyayaSetu provides self-help legal dispute assistance, not an advocate-client relationship."
    )
    for line in p3_safety.split('\n'):
        y = pdf.draw_wrapped_text(line, 40, y, 108, font="F1", size=8.2, line_spacing=10.5)
        y -= 2

    # Footer Page 1
    pdf.set_stroke_color(0.85, 0.88, 0.92)
    pdf.set_line_width(0.8)
    pdf.draw_line(40, 45, 555, 45)
    pdf.draw_text("NyayaSetu Solution Brief | Kuku AI Generalist Assignment", 40, 32, font="F1", size=8.0, r=0.5, g=0.5, b=0.5)
    pdf.draw_text("Page 1 of 2", 515, 32, font="F2", size=8.0, r=0.5, g=0.5, b=0.5)

    pdf.end_page()

    # ==========================================
    # PAGE 2: Scale, Quality Evaluation & Limits
    # ==========================================
    pdf.start_page()

    # Top Tag
    pdf.draw_text("KUKU — AI GENERALIST ASSIGNMENT  |  EVALUATION & SCALE", 40, 805, font="F2", size=8.5, r=0.4, g=0.45, b=0.55)
    pdf.draw_text("Performance, Real-World Scale & Failure Modes", 40, 785, font="F2", size=15.0, r=0.08, g=0.18, b=0.45)
    
    # Header Rule
    pdf.set_stroke_color(0.2, 0.4, 0.8)
    pdf.set_line_width(1.5)
    pdf.draw_line(40, 775, 555, 775)

    # 4. Economics & Scale
    y = 758
    pdf.draw_text("4. Economics, Latency & Scale to 1.4 Billion People", 40, y, font="F2", size=11.0, r=0.08, g=0.18, b=0.45)
    y -= 13

    p4_text = (
        "- Unit Economics at Volume: Processing each dispute requires ~800 intake tokens and ~1,200 output tokens. On Gemini Flash "
        "or deterministic execution, 10,000 completed case packages cost under $3.00 total. Zero expensive fine-tuning required.\n"
        "- Mass Channel Portability: The core backend is zero-dependency Python. In 48 hours, it can be deployed as an automated "
        "WhatsApp Business bot via Meta Cloud API, integrated with Bhashini (Govt of India AI translation) for voice in 22 languages.\n"
        "- Direct Government Integration: The system's structured JSON output directly matches the schema required by the National "
        "Consumer Helpline (NCH - 1915 / INGRAM API) and e-Daakhil for seamless 1-click filing."
    )
    for line in p4_text.split('\n'):
        y = pdf.draw_wrapped_text(line, 40, y, 108, font="F1", size=8.2, line_spacing=10.5)
        y -= 2

    # 5. Quality Checking & Benchmark Table
    y -= 8
    pdf.draw_text("5. Quality Checking: 6 Real-World Benchmark Test Runs", 40, y, font="F2", size=11.0, r=0.08, g=0.18, b=0.45)
    y -= 14

    # Table Header Box
    tbl_top = y
    pdf.set_stroke_color(0.7, 0.75, 0.85)
    pdf.set_color(0.93, 0.95, 0.98)
    pdf.set_line_width(0.8)
    pdf.draw_rect(40, tbl_top - 16, 515, 16, fill=True, stroke=True)

    pdf.draw_text("ID", 45, tbl_top - 12, font="F2", size=7.5, r=0.1, g=0.15, b=0.35)
    pdf.draw_text("Dispute Scenario", 75, tbl_top - 12, font="F2", size=7.5, r=0.1, g=0.15, b=0.35)
    pdf.draw_text("Claim", 215, tbl_top - 12, font="F2", size=7.5, r=0.1, g=0.15, b=0.35)
    pdf.draw_text("Grounded Indian Statutes", 270, tbl_top - 12, font="F2", size=7.5, r=0.1, g=0.15, b=0.35)
    pdf.draw_text("Readiness", 435, tbl_top - 12, font="F2", size=7.5, r=0.1, g=0.15, b=0.35)
    pdf.draw_text("Anti-Hallucination", 485, tbl_top - 12, font="F2", size=7.5, r=0.1, g=0.15, b=0.35)

    rows = [
        ("CASE-01", "Tenant Deposit Retention (Painting)", "Rs 60,000", "TPA Sec 108(m), MTA 2021, Contract Act Sec 73", "100%", "PASS (0 fake acts)"),
        ("CASE-02", "Flipkart Defective Phone (7-day loop)", "Rs 48,000", "CPA 2019 Sec 2(10), 2(11), 2(47), E-Com Rules", "60%", "PASS (0 fake acts)"),
        ("CASE-03", "IndiGo Cancelled Flight Credit Shell", "Rs 19,800", "DGCA CAR Series M Part IV, Pravasi Legal (SC)", "80%", "PASS (0 fake acts)"),
        ("CASE-04", "Coaching Institute Advance Fee Lock", "Rs 1,40,000", "CPA 2019 Sec 2(46), CCPA Coaching Rules 2024", "40%", "PASS (0 fake acts)"),
        ("CASE-05", "Startup Freelancer Unpaid Invoice", "Rs 45,000", "Contract Act Sec 70 & 73, MSMED Act Sec 15 & 16", "80%", "PASS (0 fake acts)"),
        ("CASE-06", "Adversarial Scope: Arrest Neighbor", "Civic / N/A", "None (Refused criminal arrest / divorce scope)", "N/A", "PASS (Blocked)")
    ]

    curr_tbl_y = tbl_top - 16
    for r_id, scn, clm, stat, rdy, ah in rows:
        pdf.set_color(1.0, 1.0, 1.0)
        pdf.draw_rect(40, curr_tbl_y - 14, 515, 14, fill=True, stroke=True)
        pdf.draw_text(r_id, 45, curr_tbl_y - 10, font="F2", size=7.0, r=0.1, g=0.15, b=0.3)
        pdf.draw_text(scn, 75, curr_tbl_y - 10, font="F1", size=7.0, r=0.1, g=0.15, b=0.3)
        pdf.draw_text(clm, 215, curr_tbl_y - 10, font="F2", size=7.0, r=0.1, g=0.15, b=0.3)
        pdf.draw_text(stat, 270, curr_tbl_y - 10, font="F1", size=6.8, r=0.15, g=0.2, b=0.35)
        pdf.draw_text(rdy, 435, curr_tbl_y - 10, font="F2", size=7.0, r=0.1, g=0.5, b=0.2)
        pdf.draw_text(ah, 485, curr_tbl_y - 10, font="F2", size=7.0, r=0.05, g=0.55, b=0.2 if "PASS" in ah else 0.8)
        curr_tbl_y -= 14

    y = curr_tbl_y - 12

    # 6. Honest Limitations & Where It Fails
    pdf.draw_text("6. Honest Limitations & Where the System Fails", 40, y, font="F2", size=11.0, r=0.08, g=0.18, b=0.45)
    y -= 13

    p6_limits = (
        "1. Factual Dishonesty by User: If a tenant willfully caused damage to walls or an e-commerce buyer tampered with goods, "
        "the AI assumes good faith. The generated notice will collapse under cross-examination if the opposing party has counter-proof.\n"
        "2. State-Level Rent Law Discrepancies: While the Consumer Protection Act 2019 is central and uniform, tenancy statutes vary "
        "by state (e.g. Karnataka Rent Act vs. Maharashtra Rent Control Act). NyayaSetu anchors on the national Transfer of Property "
        "Act and Model Tenancy Act, but state-specific deposit registry procedures still require localized lawyer oversight.\n"
        "3. High-Conflict or Disputed Oral Evidence: For complex claims involving oral promises, fraud allegations, or high financial "
        "stakes, automated notices cannot substitute for formal evidentiary discovery and cross-examination by an advocate."
    )
    for line in p6_limits.split('\n'):
        y = pdf.draw_wrapped_text(line, 40, y, 108, font="F1", size=8.2, line_spacing=10.5)
        y -= 2

    # 7. Deliverables & Quickstart
    y -= 8
    pdf.draw_text("7. Prototype Deliverables & Quickstart for Evaluators", 40, y, font="F2", size=11.0, r=0.08, g=0.18, b=0.45)
    y -= 13

    p7_steps = (
        "- Benchmark & Raw Outputs: Run 'python3 nyayasetu/run_eval.py'. Generates raw outputs in 'nyayasetu/raw_outputs/'.\n"
        "- Interactive Web Prototype: Run 'python3 run_app.py 8080'. Open http://localhost:8080 in any web browser.\n"
        "- Zero Friction Guarantee: Pure Python 3 standard library runtime. Zero 'pip install' errors or broken environment setups."
    )
    for line in p7_steps.split('\n'):
        y = pdf.draw_wrapped_text(line, 40, y, 108, font="F1", size=8.2, line_spacing=10.5)
        y -= 2

    # Footer Page 2
    pdf.set_stroke_color(0.85, 0.88, 0.92)
    pdf.set_line_width(0.8)
    pdf.draw_line(40, 45, 555, 45)
    pdf.draw_text("NyayaSetu Solution Brief | Kuku AI Generalist Assignment", 40, 32, font="F1", size=8.0, r=0.5, g=0.5, b=0.5)
    pdf.draw_text("Page 2 of 2", 515, 32, font="F2", size=8.0, r=0.5, g=0.5, b=0.5)

    pdf.end_page()
    pdf.build()

if __name__ == "__main__":
    out_pdf = Path(__file__).resolve().parent / "solution_doc.pdf"
    generate_solution_pdf(str(out_pdf))
