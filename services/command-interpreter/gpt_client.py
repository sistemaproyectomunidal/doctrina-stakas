import os
import json
from typing import Optional, Dict, Any

import httpx

GPT5_API_URL = os.getenv("GPT5_API_URL")  # e.g. https://api.yourprovider.com/v1/generate
GPT5_API_KEY = os.getenv("GPT5_API_KEY")


class GPT5Client:
    """Simple pluggable GPT-5 client.

    Uses `GPT5_API_URL` and `GPT5_API_KEY` environment variables. If not set,
    the caller should fallback to mock behavior.
    """

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self.api_url = api_url or GPT5_API_URL
        self.api_key = api_key or GPT5_API_KEY

    async def generate_action(self, instruction: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Send instruction to GPT-5 and parse a JSON action response.

        Expected response format (JSON in assistant content):
        {
          "action": "deploy_service",
          "params": {"service": "ml-engine", "env": "prod"},
          "message": "Desplegando..."
        }

        This function will try to parse JSON from the model output. If parsing fails,
        it returns a dict with action 'unknown'.
        """
        if not self.api_url or not self.api_key:
            raise RuntimeError("GPT-5 client is not configured (GPT5_API_URL / GPT5_API_KEY missing)")

        payload = {
            "input": instruction,
        }
        if system_prompt:
            payload["system_prompt"] = system_prompt

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            resp = await client.post(self.api_url, headers=headers, json=payload, timeout=30)
            text = resp.text

        # Try to parse JSON directly
        try:
            data = json.loads(text)
            # If provider wraps assistant text, try to extract
            if isinstance(data, dict) and "content" in data:
                # If content is JSON string
                try:
                    return json.loads(data["content"])
                except Exception:
                    return data
            return data
        except Exception:
            # Try to extract a JSON substring from text
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(text[start : end + 1])
                except Exception:
                    pass

        # Fallback
        return {"action": "unknown", "params": {}, "message": "No se pudo parsear la respuesta de GPT-5."}


def get_gpt5_client() -> Optional[GPT5Client]:
    if GPT5_API_URL and GPT5_API_KEY:
        return GPT5Client()
    return None
