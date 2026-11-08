"""
NyayaSetu - Pluggable LLM Interface
Enables 1-click swapping between:
1. Local Deterministic Expert Engine (Default, 0-dependency, 0-hallucination, 100% offline)
2. Google Gemini API (via standard library urllib)
3. OpenAI API (via standard library urllib)
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from .statutes import VERIFIED_STATUTES, match_domain_by_text
from .case_builder import build_case_sheet
from .rights_explainer import generate_plain_language_explanation
from .drafter import draft_legal_notice, draft_consumer_complaint_petition, draft_nch_grievance, draft_whatsapp_escalation
from .simulator import get_roleplay_scenarios

class LegalAIEngine:
    def __init__(self, model_type: str = "deterministic", api_key: Optional[str] = None):
        self.model_type = model_type.lower()
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")

    def process_case(self, user_narrative: str, language: str = "english") -> Dict[str, Any]:
        """Main end-to-end processing pipeline."""
        category = match_domain_by_text(user_narrative)
        
        # Scope / Safety Check
        if category == "out_of_scope":
            return {
                "status": "out_of_scope",
                "message": (
                    "⚠️ IMPORTANT LEGAL ESCALATION & SCOPE BOUNDARY:\n"
                    "This matter involves potential criminal allegations, physical harm, or specialized family/matrimonial dispute. "
                    "NyayaSetu is strictly an everyday consumer and civil rights assistant.\n\n"
                    "Immediate Steps Required:\n"
                    "1. For immediate safety/criminal complaints: Dial 112 (National Emergency Helpline) or visit your nearest Police Station.\n"
                    "2. For free legal aid from a certified Indian advocate: Call National Legal Services Authority (NALSA) Helpline at 15100.\n"
                    "3. For matrimonial/custody disputes: You must consult a licensed Family Court advocate. AI cannot draft criminal petitions or divorce proceedings."
                ),
                "is_safe": False,
                "domain": "Emergency / Criminal / Family Court (Out of Scope)"
            }

        # If model is external API and API key is provided, try LLM with grounded prompt
        if self.model_type in ["gemini", "openai"] and self.api_key:
            try:
                return self._call_external_llm(user_narrative, category, language)
            except Exception as e:
                # Fallback seamlessly to deterministic engine
                print(f"[Warning] External LLM call failed ({e}). Falling back to Local Deterministic Engine.")
                return self._process_deterministic(user_narrative, category, language, fallback_note=f"Fallback used: {str(e)}")
        
        return self._process_deterministic(user_narrative, category, language)

    def _process_deterministic(self, user_narrative: str, category: str, language: str, fallback_note: Optional[str] = None) -> Dict[str, Any]:
        """Guaranteed zero-hallucination deterministic pipeline."""
        case_sheet = build_case_sheet(user_narrative, category)
        rights = generate_plain_language_explanation(case_sheet, language=language)
        
        legal_notice = draft_legal_notice(case_sheet)
        consumer_petition = draft_consumer_complaint_petition(case_sheet)
        nch_text = draft_nch_grievance(case_sheet)
        whatsapp_msg = draft_whatsapp_escalation(case_sheet)
        roleplay = get_roleplay_scenarios(category)
        
        statute_info = VERIFIED_STATUTES.get(category, {})

        return {
            "status": "success",
            "model_used": "Deterministic Expert Rule Engine (Zero Hallucination Anchor)",
            "fallback_note": fallback_note,
            "category": category,
            "domain_title": statute_info.get("domain", "Everyday Consumer Grievance"),
            "case_sheet": case_sheet,
            "rights_explainer": rights,
            "legal_drafts": {
                "legal_notice": legal_notice,
                "consumer_petition": consumer_petition,
                "nch_grievance": nch_text,
                "whatsapp_escalation": whatsapp_msg
            },
            "roleplay_scenarios": roleplay,
            "statutory_references": statute_info.get("primary_statutes", []),
            "authorities": statute_info.get("authorities", []),
            "is_safe": True
        }

    def _call_external_llm(self, narrative: str, category: str, language: str) -> Dict[str, Any]:
        """Calls Gemini or OpenAI with strict statutory context injection."""
        statute_info = VERIFIED_STATUTES.get(category, {})
        statute_context = json.dumps(statute_info, indent=2)

        system_prompt = (
            "You are NyayaSetu, an AI Legal Navigator for Indian Consumers and Everyday Legal Rights.\n"
            "STRICT GROUND RULE: You must NEVER invent or hallucinate laws, IPC sections, or fake case laws.\n"
            "Ground your analysis strictly on the provided verified Indian statutes:\n"
            f"{statute_context}\n\n"
            "Respond in JSON matching the schema of Case Sheet, Rights Explainer, and Drafts."
        )

        if self.model_type == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            payload = {
                "contents": [
                    {"role": "user", "parts": [{"text": f"{system_prompt}\n\nUser Case Narrative:\n{narrative}"}]}
                ],
                "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text_content = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text_content)
                parsed["model_used"] = "Google Gemini 1.5 Flash (Grounded)"
                parsed["status"] = "success"
                return parsed

        elif self.model_type == "openai":
            url = "https://api.openai.com/v1/chat/completions"
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": narrative}
                ],
                "temperature": 0.2,
                "response_format": {"type": "json_object"}
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text_content = data["choices"][0]["message"]["content"]
                parsed = json.loads(text_content)
                parsed["model_used"] = "OpenAI GPT-4o-mini (Grounded)"
                parsed["status"] = "success"
                return parsed

        raise ValueError(f"Unsupported model type: {self.model_type}")

