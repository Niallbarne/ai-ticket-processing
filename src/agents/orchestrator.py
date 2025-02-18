import json
from datetime import datetime  # 
from nltk.sentiment import SentimentIntensityAnalyzer

class Orchestrator:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    async def process_ticket(self, ticket, user_info, response_templates):
        sentiment = self.sia.polarity_scores(ticket)
        priority_level = "High" if sentiment["compound"] < -0.2 else "Low"
        
        response = {
            "ticket": ticket,
            "priority_level": priority_level,
            "processed_at": datetime.utcnow(),  # 
        }

        return response

async def test_orchestrator():
    # Delayed import to avoid circular dependency
    from src.agents.bulk_orchestration import CustomJSONEncoder  

    sample_ticket = "I can't log in to my account. Please fix this ASAP!"
    response_templates = {
        "access": "Hello {name}, we are fixing your {feature}. Priority: {priority_level}. ETA: {eta}.",
    }

    orchestrator = Orchestrator()
    result = await orchestrator.process_ticket(sample_ticket, {"role": "Admin"}, response_templates)

    print("\n🔍 **Final Orchestrated Output:**")
    print(json.dumps(result, indent=4, cls=CustomJSONEncoder))  

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_orchestrator())
