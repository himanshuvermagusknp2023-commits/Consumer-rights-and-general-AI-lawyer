"""
NyayaSetu - Devil's Advocate / Opposing Party Roleplay Simulator
Equips everyday citizens with rehearsal scripts and counter-arguments against
intimidating pushbacks from landlords, e-commerce giants, airlines, and corporations.
"""

from typing import Dict, List, Any

SIMULATION_ROLES: Dict[str, List[Dict[str, str]]] = {
    "tenancy_deposit": [
        {
            "objection": "Look at Clause 14 of the rental agreement. You signed it, and it clearly states that one month's rent will be deducted for house painting upon vacating.",
            "intent": "Intimidation using non-negotiable standard contract clause.",
            "rebuttal_english": "Under Section 108(m) of the Transfer of Property Act and the Model Tenancy Act principles, standard wear and tear is the owner's legal responsibility. A boilerplate clause that deducts arbitrary amounts without actual damage or itemized contractor GST bills constitutes an unfair contract term under Section 23 of the Indian Contract Act. If you painted, please share the verified GST tax invoice, otherwise refund the deposit in full.",
            "rebuttal_hinglish": "Rental agreement mein likha hona kafi nahi hai. Indian law (Transfer of Property Act Sec 108m) ke hisaab se normal wear & tear landlord ki responsibility hoti hai. Bina contractor ke verified GST bill ke aap arbitrary deduction nahi kar sakte. Agar aapne paint karwaya hai toh mujhe GST bill dikhayein, varna poora deposit refund karein.",
            "statutory_anchor": "Transfer of Property Act, Sec 108(m) & Contract Act Sec 23"
        },
        {
            "objection": "Go ahead and send notices or go to court. A civil case takes 10 years in India and a lawyer will charge you ₹50,000 upfront. You will spend more than the deposit!",
            "intent": "Exploiting fear of court delays and expensive lawyer fees.",
            "rebuttal_english": "I don't need to spend ₹50,000 on a private advocate or wait 10 years. Under the Legal Services Authorities Act, 1987, I can present this before the District Lok Adalat or the Rent Authority for free with zero court fee. Furthermore, in Small Causes Court, summary recovery proceedings apply, and the court awards 12% interest plus litigation costs against the defaulting party.",
            "rebuttal_hinglish": "Mujhe ₹50,000 vakeel pe kharch karne ki zaroorat nahi hai. District Legal Services Authority (Lok Adalat) mein bina kisi court fees ke case settle hota hai. Small Causes Court mein summary procedure hota hai jismein court 12% byaaj aur legal expenses aapke upar impose karegi.",
            "statutory_anchor": "Legal Services Authorities Act, 1987 & Order XXXVII CPC"
        }
    ],
    "ecommerce_defective_goods": [
        {
            "objection": "Our platform policy clearly states '7-day replacement only, strictly no refunds'. The 7-day window has expired, so the complaint is closed.",
            "intent": "Invoking internal corporate policy to override statutory consumer rights.",
            "rebuttal_english": "Internal company policy cannot override the Consumer Protection Act, 2019. Under Section 2(10) and 2(11), supplying a defective product and failing to replace or repair it within a reasonable time constitutes gross deficiency in service. Denying a refund when replacement fails is an Unfair Trade Practice under Section 2(47), for which the Central Consumer Protection Authority has repeatedly penalized e-commerce platforms.",
            "rebuttal_hinglish": "Company ki internal policy Consumer Protection Act 2019 ke upar nahi ho sakti. Section 2(10) aur 2(11) ke tehat defective item dena aur replace na kar pana Deficiency in Service hai. Replacement fail hone ke baad refund refuse karna Section 2(47) mein Unfair Trade Practice hai.",
            "statutory_anchor": "Consumer Protection Act 2019, Sec 2(11) & Sec 2(47)"
        },
        {
            "objection": "We are only an online intermediary platform under Section 79 of the IT Act. We don't make or sell the product. You must contact the third-party seller directly.",
            "intent": "Claiming intermediary safe harbor to dodge responsibility.",
            "rebuttal_english": "Under Rule 5 and Rule 6 of the Consumer Protection (E-Commerce) Rules, 2020, marketplace platforms that collect payments, manage logistics, and handle customer communication have direct statutory liability to maintain a Grievance Redressal mechanism. You cannot claim intermediary safe harbor when you facilitate payment and fulfillment.",
            "rebuttal_hinglish": "Consumer Protection (E-Commerce) Rules, 2020 ke tehat jo platform payment aur delivery collect karta hai, uski direct legal liability banti hai. Section 79 IT Act ka safe harbor consumer grievances mein platform ko bacha nahi sakta.",
            "statutory_anchor": "Consumer Protection (E-Commerce) Rules 2020, Rule 5 & 6"
        }
    ],
    "edtech_coaching_fee": [
        {
            "objection": "You signed the admission form acknowledging that fees once paid is strictly non-refundable under any circumstances. We cannot make an exception.",
            "intent": "Citing one-sided boilerplate contract to withhold advance tuition.",
            "rebuttal_english": "The Supreme Court of India and NCDRC in landmark judgments including FIITJEE vs Minathi Nayak have explicitly held that educational institutions cannot hoard advance fees if a student withdraws mid-way. Under the CCPA Coaching Guidelines 2024 and Section 2(46) of the Consumer Protection Act 2019, a 'no refund' clause is void as an Unfair Contract. You are legally required to refund the pro-rata unutilized fee within 10 days.",
            "rebuttal_hinglish": "Supreme Court aur NCDRC ne saaf bola hai ki coaching institutes poori advance fees forfeit nahi kar sakte. CCPA Coaching Guidelines 2024 aur Section 2(46) CPA ke under 'Non-refundable' clause illegal maana gaya hai. Aapko bache huye duration ki pro-rata fees 10 din ke andar refund karni hogi.",
            "statutory_anchor": "CCPA Coaching Guidelines 2024 & CPA 2019 Sec 2(46)"
        }
    ],
    "airline_flight_refund": [
        {
            "objection": "Due to operational disruption, the ticket amount has been credited to your airline credit shell / travel wallet, valid for 6 months. It cannot be converted to bank cash.",
            "intent": "Trapping consumer money into proprietary airline vouchers.",
            "rebuttal_english": "Under DGCA CAR Section 3, Series M, Part IV and the Supreme Court ruling in Pravasi Legal Cell vs UOI (2020), airlines cannot unilaterally impose credit shells. The passenger has the absolute statutory right to choose a 100% refund into the original mode of payment. Please initiate the bank refund within 7 working days, failing which this will be filed with AirSewa and the District Consumer Commission.",
            "rebuttal_hinglish": "DGCA ke rules (CAR Series M Part IV) aur Supreme Court ke judgment ke anusar airline apni marzi se credit shell impose nahi kar sakti. Passenger ke paas poora haq hai ki wo apne bank account mein refund le. Kripya 7 working days mein bank transfer karein, varna AirSewa portal pe formal complaint daali jayegi.",
            "statutory_anchor": "DGCA CAR Series M Part IV & Pravasi Legal Cell (2020)"
        }
    ],
    "unpaid_freelance_salary": [
        {
            "objection": "We are facing a major cash crunch and waiting for our Series A funding round to close in 6 months. You have to wait until then.",
            "intent": "Passing speculative corporate financing risks onto individual workers.",
            "rebuttal_english": "Under Section 70 and Section 73 of the Indian Contract Act, operational payment for completed and approved deliverables cannot be conditioned on external speculative equity financing unless specifically written into the contract. Under commercial law, withholding earned dues attracts interest, and if registered under MSME, compound interest at 3x RBI bank rate is statutorily mandatory under Section 16 MSMED Act.",
            "rebuttal_hinglish": "Contract Act ke Section 70 ke tehat jab aapne kaam approve kar liya hai, toh payment funding pe conditional nahi ho sakti. Late payment pe statutory interest lagta hai, aur MSMED Act ke tehat RBI ke 3x compound interest ki liability aati hai.",
            "statutory_anchor": "Indian Contract Act Sec 70 & MSMED Act Sec 16"
        }
    ]
}

def get_roleplay_scenarios(category: str) -> List[Dict[str, str]]:
    """Returns simulated objections and counter-arguments for the specified category."""
    return SIMULATION_ROLES.get(category, SIMULATION_ROLES["ecommerce_defective_goods"])
