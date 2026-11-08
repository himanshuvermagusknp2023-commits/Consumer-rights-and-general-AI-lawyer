#!/usr/bin/env python3
"""
NyayaSetu - Web Prototype HTTP Server
Lightweight, zero-external-dependency web server built with standard Python library.
Serves the web application and handles REST API calls for conversational legal analysis,
the 4 Task Pillars, and interactive roleplay practice.
"""

import sys
import json
import glob
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Setup path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR.parent))

from nyayasetu.core.conversational_agent import ConversationalLegalAgent
from nyayasetu.core.llm_client import LegalAIEngine

STATIC_DIR = Path(__file__).resolve().parent / "static"

class NyayaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._serve_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
        elif path == "/api/test_cases":
            self._handle_get_test_cases()
        elif (STATIC_DIR / path.lstrip("/")).is_file():
            self._serve_static_file(STATIC_DIR / path.lstrip("/"))
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/chat":
            self._handle_chat()
        elif path == "/api/roleplay":
            self._handle_roleplay()
        elif path == "/api/analyze":
            self._handle_analyze()
        else:
            self.send_error(404, "Endpoint Not Found")

    def _serve_file(self, file_path: Path, content_type: str):
        if not file_path.exists():
            self.send_error(404, f"File {file_path.name} not found")
            return
        content = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(content)

    def _serve_static_file(self, file_path: Path):
        ext = file_path.suffix.lower()
        content_types = {
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
            ".png": "image/png",
            ".svg": "image/svg+xml"
        }
        ct = content_types.get(ext, "application/octet-stream")
        self._serve_file(file_path, ct)

    def _handle_get_test_cases(self):
        test_dir = ROOT_DIR / "test_cases"
        cases = []
        for p in sorted(test_dir.glob("*.json")):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    cases.append(json.load(f))
            except Exception:
                pass
        
        body = json.dumps(cases, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_chat(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            req_json = json.loads(post_data.decode("utf-8"))

            message = req_json.get("message", "").strip()
            history = req_json.get("history", [])
            session_state = req_json.get("session_state", {})
            language = req_json.get("language", "english")
            model_type = req_json.get("model", "deterministic")
            api_key = req_json.get("api_key", "").strip() or None

            agent = ConversationalLegalAgent(model_type=model_type, api_key=api_key)
            result = agent.process_message(
                message=message,
                history=history,
                session_state=session_state,
                language=language
            )

            self._send_json_response(result, 200)
        except Exception as e:
            self._send_json_response({"status": "error", "message": str(e)}, 500)

    def _handle_roleplay(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            req_json = json.loads(post_data.decode("utf-8"))

            user_rebuttal = req_json.get("user_rebuttal", "").strip()
            session_state = req_json.get("session_state", {})
            language = req_json.get("language", "english")
            model_type = req_json.get("model", "deterministic")
            api_key = req_json.get("api_key", "").strip() or None

            agent = ConversationalLegalAgent(model_type=model_type, api_key=api_key)
            result = agent._handle_roleplay_interaction(
                user_rebuttal=user_rebuttal,
                session_state=session_state,
                language=language
            )

            self._send_json_response(result, 200)
        except Exception as e:
            self._send_json_response({"status": "error", "message": str(e)}, 500)

    def _handle_analyze(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            req_json = json.loads(post_data.decode("utf-8"))

            narrative = req_json.get("narrative", "").strip()
            language = req_json.get("language", "english")
            model_type = req_json.get("model", "deterministic")
            api_key = req_json.get("api_key", "").strip() or None

            agent = ConversationalLegalAgent(model_type=model_type, api_key=api_key)
            pillars = agent.generate_four_pillars(narrative, language=language)

            self._send_json_response(pillars, 200)
        except Exception as e:
            self._send_json_response({"status": "error", "message": str(e)}, 500)

    def _send_json_response(self, data: dict, code: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def start_server(port: int = 8080):
    server_address = ("127.0.0.1", port)
    httpd = ThreadingHTTPServer(server_address, NyayaHandler)
    print(f"⚖️  NyayaSetu Conversational Legal AI Server running at http://127.0.0.1:{port}")
    print(f"Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    start_server(port)
