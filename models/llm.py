import logging
from typing import Optional, Dict, Any
import os
import requests
import json

logger = logging.getLogger(__name__)

class LLMManager:
    """Manage interactions with LLMs"""
    
    def __init__(self, provider="ollama", model_name="mistral"):
        self.provider = provider.lower()
        self.model_name = model_name
        
        # Set up provider-specific settings
        if self.provider == "ollama":
            self.api_base = "http://localhost:11434/api"
        elif self.provider == "openai":
            self.api_base = "https://api.openai.com/v1"
            self.api_key = os.environ.get("OPENAI_API_KEY")
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 800) -> str:
        """Generate text with the LLM"""
        if self.provider == "ollama":
            return self._generate_ollama(prompt, temperature, max_tokens)
        elif self.provider == "openai":
            return self._generate_openai(prompt, temperature, max_tokens)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _generate_ollama(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate text using Ollama API"""
        try:
            response = requests.post(
                f"{self.api_base}/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_length": max_tokens
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return ""
        except Exception as e:
            logger.error(f"Error generating text with Ollama: {e}")
            return ""
    
    def _generate_openai(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate text using OpenAI API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return ""
        except Exception as e:
            logger.error(f"Error generating text with OpenAI: {e}")
            return ""
