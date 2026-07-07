import os
import httpx
import asyncio
from typing import Dict, Any

class ArcAIGateway:
    def __init__(self):
        # Load environment keys for external networks
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.headers = {"Content-Type": "application/json"}

    async def query_external_intelligence(self, provider: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Routes processing requests from Random or Sai to external AI providers.
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            if provider.lower() == "openai":
                url = "https://api.openai.com/v1/chat/completions"
                headers = {**self.headers, "Authorization": f"Bearer {self.openai_api_key}"}
                response = await client.post(url, json=payload, headers=headers)
                
            elif provider.lower() == "anthropic":
                url = "https://api.anthropic.com/v1/messages"
                headers = {
                    **self.headers, 
                    "x-api-key": self.anthropic_api_key,
                    "anthropic-version": "2023-06-01"
                }
                response = await client.post(url, json=payload, headers=headers)
            
            else:
                raise ValueError(f"Unknown external provider: {provider}")
                
            return response.json()

# Example Integration for Subsystems
async def main():
    gateway = ArcAIGateway()
    
    # Example payload from Sai (requesting structural design critique)
    sai_payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "Critique this modular structural framing vector..."}]
    }
    
    # Asynchronous dispatch
    print("[Arc] Dispatching internal engine payload to external node...")
    result = await gateway.query_external_intelligence("openai", sai_payload)
    print("[Arc] External response integrated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
