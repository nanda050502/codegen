"""
Ollama Integration Service
Handles all interactions with the local Ollama API
"""

import ollama
import requests
import time
from typing import Dict, List, Tuple, Optional
import re
from datetime import datetime


class OllamaService:
    """Service for interacting with local Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self.best_model = None
        
    def check_availability(self) -> Tuple[bool, List[str]]:
        """Check if Ollama is running and get available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.available_models = [model['name'] for model in data.get('models', [])]
                return True, self.available_models
            return False, []
        except Exception as e:
            print(f"❌ Ollama check error: {e}")
            return False, []
    
    def select_best_model(self) -> Optional[str]:
        """Select the best available model for code generation"""
        # Priority order for code generation
        preferred_models = [
            "codellama",
            "deepseek-coder",
            "mistral",
            "llama3",
            "phi",
            "qwen"
        ]
        
        for preferred in preferred_models:
            for available in self.available_models:
                if preferred in available.lower():
                    self.best_model = available
                    return available
        
        # Return first available model as fallback
        if self.available_models:
            self.best_model = self.available_models[0]
            return self.available_models[0]
        
        return None
    
    def generate_code(
        self,
        prompt: str,
        language: str,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1000
    ) -> Dict:
        """
        Generate code using Ollama
        
        Returns:
            Dict with keys: success, code, raw_output, time_ms, model, error
        """
        start_time = time.time()
        
        if model is None:
            model = self.best_model or self.select_best_model()
        
        if not model:
            return {
                "success": False,
                "code": "",
                "raw_output": "",
                "time_ms": 0,
                "model": None,
                "error": "No Ollama model available"
            }
        
        # Language-specific system prompts
        system_prompts = {
            "python": "You are an expert Python developer. Generate clean, efficient Python code following PEP 8 standards.",
            "javascript": "You are an expert JavaScript developer. Generate modern ES6+ JavaScript code.",
            "typescript": "You are an expert TypeScript developer. Generate type-safe TypeScript code.",
            "java": "You are an expert Java developer. Generate clean, object-oriented Java code.",
            "cpp": "You are an expert C++ developer. Generate modern C++17/20 code.",
            "rust": "You are an expert Rust developer. Generate safe, idiomatic Rust code.",
            "go": "You are an expert Go developer. Generate clean, idiomatic Go code.",
            "csharp": "You are an expert C# developer. Generate clean, modern C# code.",
        }
        
        system_prompt = system_prompts.get(
            language.lower(),
            f"You are an expert {language} developer. Generate clean, well-documented code."
        )
        
        try:
            print(f"🔄 Generating code with {model}...")
            
            response = ollama.chat(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": f"{system_prompt}\n\nIMPORTANT: Return ONLY the code. No explanations, no markdown formatting, no instructions. Just the raw code."
                    },
                    {
                        "role": "user",
                        "content": f"Generate {language} code for: {prompt}\n\nReturn ONLY the code itself. No text before or after."
                    }
                ],
                options={
                    "temperature": temperature,
                    "top_p": 0.9,
                    "num_predict": max_tokens
                }
            )
            
            raw_output = response['message']['content']
            clean_code = self._extract_clean_code(raw_output, language)
            
            end_time = time.time()
            time_ms = int((end_time - start_time) * 1000)
            
            print(f"✅ Code generated in {time_ms}ms")
            
            return {
                "success": True,
                "code": clean_code,
                "raw_output": raw_output,
                "time_ms": time_ms,
                "model": model,
                "error": None
            }
            
        except Exception as e:
            end_time = time.time()
            time_ms = int((end_time - start_time) * 1000)
            
            print(f"❌ Error during generation: {e}")
            
            return {
                "success": False,
                "code": "",
                "raw_output": "",
                "time_ms": time_ms,
                "model": model,
                "error": str(e)
            }
    
    def _extract_clean_code(self, raw_output: str, language: str) -> str:
        """Extract clean code from Ollama response"""
        if not raw_output or not raw_output.strip():
            return ""
        
        # Remove markdown code blocks if present
        code_block_pattern = r'```(?:\w+)?\s*\n(.*?)```'
        code_blocks = re.findall(code_block_pattern, raw_output, re.DOTALL)
        
        if code_blocks:
            # Use the largest code block
            largest_block = max(code_blocks, key=len)
            return largest_block.strip()
        
        # Remove common explanation phrases
        lines = raw_output.split('\n')
        code_lines = []
        skip_phrases = [
            'here is', 'here\'s', 'this code', 'to run', 'to use', 'to save',
            'you can', 'simply', 'make sure', 'note that', 'explanation',
            'how to', 'save this', 'run this', 'execute', 'to get started'
        ]
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Skip empty lines at the start
            if not code_lines and not line.strip():
                continue
            
            # Skip explanation lines
            is_explanation = any(phrase in line_lower for phrase in skip_phrases)
            
            # Keep lines that look like code
            if not is_explanation or any(
                keyword in line for keyword in [
                    'def ', 'class ', 'function ', 'const ', 'let ', 'var ',
                    'import ', 'from ', '#include', 'public ', 'private ',
                    'fn ', 'func ', 'package ', 'using ', 'namespace '
                ]
            ):
                code_lines.append(line)
        
        final_code = '\n'.join(code_lines).strip()
        
        # If extraction resulted in very short code, return raw output
        if not final_code or len(final_code) < 10:
            return raw_output.strip()
        
        return final_code
    
    def stream_generate(self, prompt: str, language: str, model: Optional[str] = None):
        """Generator function for streaming code generation (for WebSocket)"""
        if model is None:
            model = self.best_model or self.select_best_model()
        
        if not model:
            yield {"type": "error", "content": "No model available"}
            return
        
        try:
            stream = ollama.chat(
                model=model,
                messages=[
                    {"role": "user", "content": f"Generate {language} code for: {prompt}"}
                ],
                stream=True
            )
            
            for chunk in stream:
                content = chunk['message']['content']
                yield {"type": "content", "content": content}
            
            yield {"type": "complete"}
            
        except Exception as e:
            yield {"type": "error", "content": str(e)}


# Singleton instance
ollama_service = OllamaService()
