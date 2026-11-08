"""
NyayaSetu - Plain Language Rights Explainer
Explains legal standing, statutory rights, escalation steps, and realistic timelines
in accessible English and conversational Hinglish.
"""

from typing import Dict, Any
from .statutes import VERIFIED_STATUTES

def generate_plain_language_explanation(case: Dict[str, Any], language: str = "english") -> Dict[str, Any]:
    cat = case.get("category", "ecommerce_defective_goods")
    amount = case.get("principal_claim_amount", 0)
    statute_info = VERIFIED_STATUTES.get(cat, {})
    
    if language == "hinglish":
        return _generate_hinglish_explanation(case, statute_info)
    else:
        return _generate_english_explanation(case, statute_info)

def _generate_english_explanation(case: Dict[str, Any], statute_info: Dict[str, Any]) -> Dict[str, Any]:
    domain = statute_info.get("domain", "Consumer Rights")
    statutes = statute_info.get("primary_statutes", [])
    authorities = statute_info.get("authorities", [])
    limitation = statute_info.get("limitation_period", "2-3 years under statutory limitation")
    amount = case.get("principal_claim_amount", 0)

    # Statutory summary bullets
    rights_bullets = []
    for s in statutes:
        for r in s.get("rules", []):
            rights_bullets.append(f"**{s.get('act')} ({s.get('section')})**: {r}")

    standing_summary = (
        f"You have a strong legal standing under Indian civil and consumer law. "
        f"Under {domain}, withholding your legitimate funds of ₹{amount:,} or failing to deliver contracted quality "
        f"is legally actionable. Indian law does not allow unilateral contract clauses or arbitrary forfeitures."
    )

    escalation_path = [
        {
            "tier": "Step 1: Formal Statutory Demand Notice (15-Day Cure Period)",
            "action": "Dispatch a formal legal notice via Registered Post AD / Speed Post and Email. Give them 15 working days to refund ₹" + f"{amount:,} plus interest.",
            "why_it_works": "Over 75% of Indian consumer & tenancy disputes settle at this stage once the opposite party sees precise statutory sections and realizes you are prepared to escalate.",
            "cost": "₹0 to ₹50 (Speed post charges)"
        },
        {
            "tier": "Step 2: National Consumer Helpline (NCH 1915) / Statutory Portal",
            "action": f"File a grievance on consumerhelpline.gov.in (Toll-Free 1915) or {'AirSewa' if 'airline' in case.get('category','') else 'INGRAM portal'}.",
            "why_it_works": "Government officers directly notify the nodal officer of the registered corporate entity, requiring a mandatory written status update within 30 days.",
            "cost": "Free (Government initiative)"
        },
        {
            "tier": "Step 3: Online e-Daakhil / District Consumer Commission (DCDRC)",
            "action": "File an e-complaint on e-daakhil.nic.in before the District Consumer Forum. Under the Consumer Protection Act 2019, claims up to ₹5 Lakh have ZERO court fees.",
            "why_it_works": "You do NOT need to hire an expensive advocate; consumers can represent themselves. The forum can award refund + 9-12% interest + compensation for mental harassment.",
            "cost": "₹0 (for claims up to ₹5L), ₹200 for claims up to ₹10L"
        }
    ]

    return {
        "domain": domain,
        "standing_summary": standing_summary,
        "key_rights": rights_bullets,
        "authorities": authorities,
        "limitation_period": limitation,
        "escalation_path": escalation_path,
        "realistic_timeline": "15 days for initial notice response; 30 to 45 days if escalated via NCH; 3 to 6 months for formal Consumer Commission order.",
        "financial_outlook": f"Eligible to claim full ₹{amount:,} + 9-12% annual interest + ₹15,000 to ₹25,000 for mental agony & litigation costs."
    }

def _generate_hinglish_explanation(case: Dict[str, Any], statute_info: Dict[str, Any]) -> Dict[str, Any]:
    domain = statute_info.get("domain", "Consumer Rights")
    amount = case.get("principal_claim_amount", 0)

    standing_summary = (
        f"Aapka case Indian Law ke hisaab se kaafi strong hai. "
        f"{domain} ke tehat aapka ₹{amount:,} rokna ya unfair terms impose karna illegal hai. "
        f"Koyi bhi company ya landlord apni marzi se 'non-refundable' bol kar aapka haq nahi chheen sakta."
    )

    escalation_path = [
        {
            "tier": "Step 1: Formal Legal Notice bhejna (15 Din ka Time)",
            "action": f"Opposite party ko Speed Post aur Email ke zariye formal demand notice bhejein, jismein ₹{amount:,} aur interest ka claim ho.",
            "why_it_works": "75% se zyada cases yahin solve ho jaate hain kyunki opposite party ko samajh aa jaata hai ki aapko exact Indian law pata hai.",
            "cost": "₹0 - ₹50 (Speed Post ka kharcha)"
        },
        {
            "tier": "Step 2: National Consumer Helpline (NCH 1915) pe Complaint",
            "action": "National Consumer Helpline (1915 ya INGRAM portal) pe direct complaint register karein.",
            "why_it_works": "Sarkar ke grievance officers seedhe company ke Nodal Officer se jawab maangte hain.",
            "cost": "Bilkul Free (Sarkari Portal)"
        },
        {
            "tier": "Step 3: e-Daakhil Portal se Consumer Court mein Case",
            "action": "e-daakhil.nic.in pe District Consumer Commission ke samne online petition file karein.",
            "why_it_works": "₹5 Lakh tak ke claims ke liye court fee ZERO hai, aur aapko mehnge vakeel ki zaroorat nahi hai. Aap khud apna case lad sakte hain.",
            "cost": "Zero court fees (up to ₹5 Lakh claim)"
        }
    ]

    return {
        "domain": domain,
        "standing_summary": standing_summary,
        "key_rights": [
            "Normal wear and tear ke naam pe landlord security deposit nahi kaat sakta bina itemized GST bill ke.",
            "Consumer Protection Act 2019 ke section 2(11) aur 2(47) ke under service deficiency aur unfair trade practice dono punishable hain.",
            "Non-refundable clause 'Unfair Contract' ke under void maana jaata hai."
        ],
        "authorities": statute_info.get("authorities", []),
        "limitation_period": "2 saal ke andar complaint karni hoti hai.",
        "escalation_path": escalation_path,
        "realistic_timeline": "15 din demand notice ka time, 30-45 din NCH resolution, ya 3-6 mahine Consumer Forum order.",
        "financial_outlook": f"Aap ₹{amount:,} principal + 9-12% byaaj (interest) + ₹15,000-₹25,000 compensation claim kar sakte hain."
    }

