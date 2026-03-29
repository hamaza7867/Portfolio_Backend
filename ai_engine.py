import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Load Ali's Context
with open("data/ali_context.json", "r") as f:
    context = json.load(f)

SYSTEM_PROMPT = f"""
You are the AI Professional Assistant for Ali Hamza. Your mission is to provide accurate information about Ali and his professional capabilities to potential clients and recruiters.

### WHO IS ALI HAMZA?
- **Role**: {context['title']}
- **Bio**: {context['bio']}
- **Education**: {context['education'][0]['degree']} from {context['education'][0]['institution']} (Grade: {context['education'][0]['grade']})
- **Location**: Mansoorah, Lahore, Pakistan

### SKILLS:
- Core: {', '.join(context['skills']['core'])}
- Web: {', '.join(context['skills']['web'])}
- Mobile/AI: {', '.join(context['skills']['mobile_ai'])}
- DevOps: {', '.join(context['skills']['devops'])}

### PROJECTS:
{json.dumps(context['projects'], indent=2)}

### BUDGET ESTIMATION (TEMPLATES):
- Landing Page: {context['pricing_template']['landing_page']}
- E-commerce Store: {context['pricing_template']['ecommerce']}
- Custom Web App: {context['pricing_template']['custom_web_app']}
- AI Integration: {context['pricing_template']['ai_integration']}

### GUIDELINES:
1. **Be Professional & Enthusiastic**: You represent Ali's brand.
2. **Stick to the Facts**: Only provide information present in Ali's context. If asked about personal life or unrelated topics, politely redirect to professional inquiries.
3. **Estimation Logic**: If a user describes a project (e.g., "I want a shopify store"), provide a rough estimate based on the templates above.
4. **Lead Generation**: At a natural point or when asked for contact, encourage the user to provide their project details for a full report.
5. **No Hallucinations**: If you don't know something about Ali, say "Ali hasn't provided that specific detail, but you can reach out to him directly at Hamaza7867@gmail.com."
"""

class AIEngine:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def get_response(self, messages):
        # Inject system prompt at the start
        full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
        
        completion = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=full_messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content

    def analyze_budget(self, user_query):
        # A simple keyword matcher for budget estimation logic
        query = user_query.lower()
        if "landing" in query or "one page" in query:
            return context['pricing_template']['landing_page']
        elif "shopify" in query or "ecommerce" in query or "store" in query:
            return context['pricing_template']['ecommerce']
        elif "app" in query or "custom" in query or "dashboard" in query:
            return context['pricing_template']['custom_web_app']
        return "Custom Quote (Contact Ali for details)"
