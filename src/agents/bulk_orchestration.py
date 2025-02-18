import json
from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

async def process_bulk_tickets(tickets, user_info, response_templates):
    
    from src.agents.orchestrator import Orchestrator  

    orchestrator = Orchestrator()
    results = []
    for ticket in tickets:
        result = await orchestrator.process_ticket(ticket, user_info, response_templates)
        results.append(result)
    
    return json.dumps(results, indent=4, cls=CustomJSONEncoder)

if __name__ == "__main__":
    import asyncio

    tickets = [
        "I can't log in to my account!",
        "Payment issue with my subscription."
    ]
    user_info = {"role": "Admin"}
    response_templates = {
        "access": "Hello {name}, we are fixing your {feature}. Priority: {priority_level}. ETA: {eta}.",
    }

    # Run the function and print the result
    print(asyncio.run(process_bulk_tickets(tickets, user_info, response_templates)))
