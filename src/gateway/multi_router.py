import os
import httpx
import asyncio
from typing import Dict, Any

class ArcMultiGateway:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        # Copilot can be leveraged via standard Azure OpenAI or GitHub API endpoints
        self.azure_copilot_key = os.getenv("AZURE_COPILOT_KEY")
        self.azure_endpoint = os.getenv("AZURE_COPILOT_ENDPOINT") 

    async def POST(self, client: httpx.AsyncClient, url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = await client.post(url, json=payload, headers=headers, timeout=45.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP Error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Connection failed: {str(e)}"}

    async def route_request(self, target: str, prompt: str, system_instruction: str = "You are a sub-node of Arc OS.") -> Dict[str, Any]:
        """
        Dispatches tasks from Random (Forex) or Sai (Architecture) to specialized external models.
        """
        async with httpx.AsyncClient() as client:
            
            # 1. CHATGPT (OpenAI)
            if target.lower() == "chatgpt":
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "gpt-4o",
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ]
                }
                return await self.POST(client, url, headers, payload)

            # 2. DEEPSEEK (DeepSeek-V3 or DeepSeek-R1 Reasoner)
            elif target.lower() == "deepseek":
                url = "https://api.deepseek.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.deepseek_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "deepseek-reasoner", # Uses R1-style deep thinking for logic/quant math
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ]
                }
                return await self.POST(client, url, headers, payload)

            # 3. COPILOT / AZURE OPENAI INTERFACE
            elif target.lower() == "copilot":
                if not self.azure_endpoint:
                    return {"error": "Azure/Copilot endpoint configuration missing."}
                url = f"{self.azure_endpoint}/openai/deployments/copilot-model/chat/completions?api-version=2024-02-15-preview"
                headers = {"api-key": self.azure_copilot_key, "Content-Type": "application/json"}
                payload = {
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ]
                }
                return await self.POST(client, url, headers, payload)

            else:
                return {"error": f"Target framework '{target}' not supported."}

# Orchestration pipeline testing parallel dispatch
async def run_network_sync():
    gateway = ArcMultiGateway()
    
    # Random delegates complex risk math to DeepSeek's reasoning engine
    random_task = gateway.route_request(
        target="deepseek",
        prompt="Analyze risk parameters for an MT5 trading sequence under high volatility.",
        system_instruction="You are the quantitative processing arm of Arc (Subsystem: Random)."
    )
    
    # Sai delegates spatial logic validation to ChatGPT
    sai_task = gateway.route_request(
        target="chatgpt",
        prompt="Verify structural redundancy constraints for a modular 3D frame vector.",
        system_instruction="You are the architectural validation arm of Arc (Subsystem: Sai)."
    )
    
    print("[Arc] Broad-network synchronization initiated...")
    results = await asyncio.gather(random_task, sai_task)
    
    print(f"[DeepSeek/Random Result]: {results[0]}")
    print(f"[ChatGPT/Sai Result]: {results[1]}")

if __name__ == "__main__":
    asyncio.run(run_network_sync())
