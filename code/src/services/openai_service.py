import openai
from typing import Dict, Any, Optional
import json
from config.config import Config

class OpenAIService:
    def __init__(self):
        # Set OpenAI API key
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        self.system_prompt = """You are an AI support assistant for the Integrated Platform Environment (IPE).
        You have access to various data sources including:
        - Incidents and tickets
        - Knowledge base articles
        - System logs
        - Automation tasks and their status
        
        Your role is to:
        1. Analyze the provided context from all available sources
        2. Provide comprehensive responses that consider all relevant information
        3. Suggest appropriate actions or next steps when applicable
        4. Reference specific incidents, tickets, or KB articles when relevant
        5. Highlight any automation tasks that might help resolve the issue
        
        When discussing tickets:
        - Use the exact ticket statistics provided in the context
        - Be precise with numbers and status counts
        - Reference specific ticket IDs when available
        - If a specific ticket is not found, explain that it's not in the current dataset
        - Provide relevant ticket statistics or similar tickets when available
        
        Always maintain a professional and helpful tone while providing clear, actionable information."""

    def get_completion(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Get completion from OpenAI API with enhanced context handling
        Args:
            prompt: The user's prompt
            context: Optional dictionary containing relevant context from various sources
        Returns:
            str: The AI's response
        """
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]

            # Add context to the conversation if available
            if context:
                context_message = "Here is the relevant context from various sources:\n"

                # Add ticket statistics if available
                if 'ticket_stats' in context:
                    stats = context['ticket_stats']
                    context_message += "\nTicket Statistics:\n"
                    context_message += f"- Total Tickets: {stats['total_tickets']}\n"
                    context_message += "- Status Distribution:\n"
                    for status, count in stats['status_counts'].items():
                        context_message += f"  * {status}: {count}\n"
                    context_message += "- Priority Distribution:\n"
                    for priority, count in stats['priority_counts'].items():
                        context_message += f"  * {priority}: {count}\n"
                    context_message += "- Component Distribution:\n"
                    for component, count in stats['component_counts'].items():
                        context_message += f"  * {component}: {count}\n"

                # Add incidents context
                if 'incidents' in context and not context['incidents'].empty:
                    context_message += "\nRelevant Incidents:\n"
                    for _, incident in context['incidents'].iterrows():
                        context_message += f"- {incident['title']} ({incident['status']})\n"

                # Add KB articles context
                if 'kb_articles' in context and not context['kb_articles'].empty:
                    context_message += "\nRelevant Knowledge Base Articles:\n"
                    for _, article in context['kb_articles'].iterrows():
                        context_message += f"- {article['title']}\n"

                # Add tickets context
                if 'tickets' in context and not context['tickets'].empty:
                    context_message += "\nRelevant Tickets:\n"
                    for _, ticket in context['tickets'].iterrows():
                        context_message += f"- {ticket['ticket_id']}: {ticket['title']} ({ticket['status']})\n"
                        context_message += f"  Priority: {ticket['priority']}, Component: {ticket['component']}\n"
                else:
                    context_message += "\nNo specific tickets found matching your query.\n"

                # Add logs context
                if 'logs' in context and context['logs']:
                    context_message += "\nRelevant Logs:\n"
                    for log in context['logs']:
                        context_message += f"- {log.get('timestamp', '')}: {log.get('message', '')}\n"

                # Add automation tasks context
                if 'automation_tasks' in context and context['automation_tasks']:
                    context_message += "\nRelevant Automation Tasks:\n"
                    for task in context['automation_tasks']:
                        context_message += f"- {task.get('description', '')} ({task.get('status', '')})\n"

                messages.insert(1, {"role": "system", "content": context_message})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            print(f"OpenAI API error: {str(e)}")
            return "I apologize, but I encountered an error while processing your request. Please try again later."
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return "I apologize, but I encountered an unexpected error. Please try again later."