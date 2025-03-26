from typing import Dict, Any
import json

class ContextEngine:
    def __init__(self):
        self.current_context = {
            "incident": None,
            "ci": None,
            "telemetry": {},
            "related_incidents": []
        }

    def update_context(self, **kwargs):
        self.current_context.update(kwargs)

    def get_current_context(self) -> Dict[str, Any]:
        return self.current_context

    def enhance_prompt(self, prompt: str, context: Dict[str, Any]) -> str:
        """Enhance the user prompt with relevant context"""
        context_str = json.dumps(context, indent=2)
        
        enhanced_prompt = f"""
        Context:
        {context_str}

        User Query:
        {prompt}

        Please provide a response considering the above context.
        """
        
        return enhanced_prompt

    def clear_context(self):
        self.__init__() 