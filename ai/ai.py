import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv

from google_services.google_api import get_calendar_service, get_gmail_service
from google_services.calendar import CalendarService
from ai.contexts.main_agent_systemPrompt import response_json_format
from ai.contexts.main_agent_systemPrompt import query_intent_action_systemPrompt

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
CONTEXT_FILE = os.getenv("CONTEXT_FILE")

class OllamaAssistant:
    def __init__(self):
        self.calendar_service = get_calendar_service()
        self.gmail_service = get_gmail_service()
        self.context = self.load_context()

    def load_context(self) -> list:
        try:
            with open(CONTEXT_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_context(self, messages: list):
        with open(CONTEXT_FILE, "w") as file:
            json.dump(messages, file, indent=2)

    def query_intent_and_action(self, user_input: str) -> Dict[str, str]:
        """Laat Ollama de intentie én actie bepalen van de input"""
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": MODEL_NAME,
                    "messages": [query_intent_action_systemPrompt, {"role": "user", "content": user_input}],
                    "stream": False
                },
                timeout=100
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "").strip()
                return json.loads(content)
            return {"intent": "general", "action": "chat"}

        except Exception as e:
            return {"intent": "general", "action": "chat"}

    def chat_response(self, system_prompt: str, json_input: str) -> str:
        self.context = [
            system_prompt,
            {"role": "user", "content": json.dumps(json_input)}
        ]
        try:
            payload = {
                "model": MODEL_NAME,
                "messages": self.context,
                "stream": False
            }

            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json=payload,
                timeout=100
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "Geen antwoord.")
                self.context.append({"role": "assistant", "content": content})
                self.save_context(self.context)
                return content
            return f"Error: Ollama responded with {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: Failed to connect to Ollama - {str(e)}"

    def handle_request(self, user_input: str) -> Dict[str, Any]:
        intent = self.query_intent_and_action(user_input)
        print(intent)
        calendar = CalendarService()
        request = calendar.handle_calendar_request(intent)

        if intent['intent'] == "calendar":
            ai_response = self.chat_response(response_json_format, request["event"])
            return { "intent": intent, "ai_response": ai_response }
        elif intent['intent'] == "email":
            # Handle email intent
            pass
        elif intent['intent'] == "general":
            return { "intent": intent, "ai_response": self.chat_response(response_json_format, intent) }