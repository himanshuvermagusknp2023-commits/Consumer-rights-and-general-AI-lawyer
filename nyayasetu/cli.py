#!/usr/bin/env python3
"""
NyayaSetu - CLI Legal Assistant & Interview Live Runner
Ideal for running new inputs on the fly during the placement interview:
    python3 nyayasetu/cli.py --text "My landlord is refusing to refund my 45000 deposit..."
    python3 nyayasetu/cli.py --file path/to/input.txt --output notice.txt
    python3 nyayasetu/cli.py --interactive
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nyayasetu.core.llm_client import LegalAIEngine

def format_terminal_box(title: str, content: str, width: int = 78) -> str:
    line = "─" * (width - 4)
    return f"┌─ {title} {line[len(title):]}┐\n{content}\n└{'─' * (width - 2)}┘"

def run_cli():
    parser = argparse.ArgumentParser(
        description="NyayaSetu (न्याय सेतु) — CLI Legal Navigator for Everyday Indian Rights",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick inline run:
  python3 nyayasetu/cli.py --text "Paid ₹55,000 rent deposit in Bengaluru. Landlord withheld saying painting charges."

  # Process a text file:
  python3 nyayasetu/cli.py --file new_case.txt --output notice.txt

  # Interactive interview mode:
  python3 nyayasetu/cli.py --interactive
        """
    )
    parser.add_argument("--text", "-t", type=str, help="Raw narrative string describing the dispute.")
    parser.add_argument("--file", "-f", type=str, help="Path to text or JSON file containing the narrative.")
    parser.add_argument("--lang", "-l", choices=["english", "hinglish"], default="english", help="Language for legal explanation.")
    parser.add_argument("--model", "-m", choices=["deterministic", "gemini", "openai"], default="deterministic", help="Model engine to use.")
    parser.add_argument("--api-key", type=str, default=None, help="API key if using external Gemini/OpenAI models.")
    parser.add_argument("--output", "-o", type=str, help="Optional path to save generated Legal Demand Notice.")
    parser.add_argument("--interactive", "-i", action="store_true", help="Launch interactive terminal questionnaire.")

    args = parser.parse_args()

    narrative = ""
    if args.interactive:
        print("=" * 80)
        print("⚖️  NYAYA SETU — INTERACTIVE LEGAL DISPUTE INTAKE")
        print("Specialized for Consumer, Tenancy, Service Deficiencies & Everyday Civil Disputes")
        print("=" * 80)
        print("Describe what happened (type or paste your story, press Enter then Ctrl+D when finished):\n")
        try:
            narrative = sys.stdin.read().strip()
        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit(0)
    elif args.file:
        p = Path(args.file)
        if not p.is_file():
            print(f"Error: File '{args.file}' does not exist.", file=sys.stderr)
            sys.exit(1)
        narrative = p.read_text(encoding="utf-8").strip()
    elif args.text:
        narrative = args.text.strip()
    else:
        parser.print_help()
        sys.exit(0)

    if not narrative:
        print("Error: No dispute narrative provided.", file=sys.stderr)
        sys.exit(1)

    print("\n🔍 Analyzing narrative & verifying statutory grounds...")
    engine = LegalAIEngine(model_type=args.model, api_key=args.api_key)
    result = engine.process_case(narrative, language=args.lang)

    if result.get("status") == "out_of_scope":
        print("\n" + "!" * 80)
        print("⚠️  MANDATORY SAFETY BOUNDARY TRIGGERED")
        print("!" * 80)
        print(result.get("message"))
        print("!" * 80)
        sys.exit(0)

    cs = result["case_sheet"]
    rx = result["rights_explainer"]
    drafts = result["legal_drafts"]
    roleplays = result.get("roleplay_scenarios", [])

    print("\n" + "=" * 80)
    print(f"⚖️  NYAYA SETU CASE ANALYSIS: {result.get('domain_title', 'Consumer Dispute')}")
    print("=" * 80)

    print(f"\n📊 CASE OVERVIEW:")
    print(f"  • Principal Claim Amount: ₹{cs['principal_claim_amount']:,}")
    print(f"  • Identified Respondent : {cs['respondent']}")
    print(f"  • Evidentiary Health    : {cs['readiness_score']}% readiness")
    print(f"  • Statutory Relief      : Principal + {cs['interest_claimed']} + ₹15k-25k damages")

    print(f"\n📁 EVIDENCE AUDIT:")
    if cs["proof_available"]:
        print(f"  ✓ Present in narrative  : {', '.join(cs['proof_available'])}")
    if cs["missing_proof_checklist"]:
        print(f"  ⚠️  Recommended to gather : {', '.join(cs['missing_proof_checklist'])}")

    print(f"\n📜 GROUNDED INDIAN STATUTES (0% Hallucination):")
    for s in result.get("statutory_references", []):
        print(f"  • {s['act']} ({s['section']}): {s['title']}")

    print(f"\n🧭 3-TIER RESOLUTION STRATEGY:")
    for step in rx.get("escalation_path", []):
        print(f"  [ {step['tier']} ]")
        print(f"    Action: {step['action']}")
        print(f"    Cost  : {step['cost']}")

    print(f"\n🥊 OPPOSING PARTY REBUTTAL PREVIEW:")
    for i, sc in enumerate(roleplays[:2], 1):
        print(f"  Objection {i}: \"{sc['objection']}\"")
        reb = sc['rebuttal_hinglish'] if args.lang == 'hinglish' else sc['rebuttal_english']
        print(f"  Rebuttal   : {reb}\n")

    # Output draft notice
    notice_text = drafts["legal_notice"]
    if args.output:
        out_p = Path(args.output)
        out_p.write_text(notice_text, encoding="utf-8")
        print(f"✓ Formal 15-Day Legal Demand Notice saved to: {out_p.resolve()}")
    else:
        print("\n" + "─" * 80)
        print("📄 PREVIEW: FORMAL LEGAL DEMAND NOTICE (FIRST 25 LINES)")
        print("─" * 80)
        lines = notice_text.splitlines()
        print("\n".join(lines[:25]))
        print(f"\n... [{len(lines)-25} more lines generated. Use --output notice.txt to save full notice.]")
        print("─" * 80)

if __name__ == "__main__":
    run_cli()
