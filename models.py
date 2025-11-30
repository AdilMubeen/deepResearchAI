"""LLM client wrappers for GPT-4, Claude, and Gemini."""
from openai import AzureOpenAI
from anthropic import Anthropic
import google.generativeai as genai
from config import Config


class Models:
    """Unified interface for all LLM providers."""
    
    def __init__(self):
        # GPT-4 via Azure OpenAI
        self.azure_client = AzureOpenAI(
            api_key=Config.AZURE_OPENAI_KEY,
            api_version=Config.AZURE_OPENAI_VERSION,
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
        )
        # Claude via Anthropic
        self.anthropic_client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        # Gemini via Google
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def gpt4_call(self, messages, temperature=0.7, max_tokens=8000):
        """Query generation and report synthesis."""
        try:
            response = self.azure_client.chat.completions.create(
                model=Config.AZURE_OPENAI_DEPLOYMENT,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"GPT-4 error: {e}")
            return None

    def claude_call(self, system_prompt, user_message, temperature=0.3, max_tokens=8000):
        """Risk analysis across 6 categories."""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Claude error: {e}")
            return None

    def gemini_call(self, prompt, temperature=0.5, max_tokens=4000):
        """Entity and timeline extraction."""
        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config={"temperature": temperature, "max_output_tokens": max_tokens}
            )
            return response.text
        except Exception as e:
            print(f"Gemini error: {e}")
            return None


models = Models()
