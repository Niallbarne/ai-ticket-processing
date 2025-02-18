import asyncio
import json
from src.agents.ticket_analysis import TicketAnalysisAgent
from src.agents.response_generation import ResponseAgent

async def process_ticket(ticket_content, customer_info, response_templates):
    """
    Processes a single support ticket by analyzing it and generating a response.

    Args:
        ticket_content (str): The text of the support ticket.
        customer_info (dict): Information about the customer (e.g., role, name).
        response_templates (dict): Predefined templates for generating responses.

    Returns:
        dict: A dictionary containing the ticket analysis and generated response.

    Example:
        response_templates = {"access": "Hello {name}, we are fixing your {feature}. Priority: {priority_level}. ETA: {eta}."}
        result = await process_ticket("I can't log in to my account.", {"role": "Admin"}, response_templates)
    """
    analysis_agent = TicketAnalysisAgent()
    response_agent = ResponseAgent()

    print("\n🔹 **Step 1: Analyzing Ticket**")
    ticket_analysis = await analysis_agent.analyze_ticket(ticket_content, customer_info)

    print("\n🔹 **Step 2: Generating Response**")
    response = await response_agent.generate_response(ticket_analysis, response_templates, {"customer_name": "Customer"})

    return {"ticket_analysis": ticket_analysis.__dict__, "response": response}

async def test_orchestrator():
    """
    Runs a test to process a sample support ticket.
    Prints the final analyzed ticket details and generated response.
    """
    sample_ticket = "I can't log in to my account. Please fix this ASAP!"
    response_templates = {
        "access": "Hello {name}, we are fixing your {feature}. Priority: {priority_level}. ETA: {eta}.",
    }
    result = await process_ticket(sample_ticket, {"role": "Admin"}, response_templates)

    print("\n🔍 **Final Orchestrated Output:**")
    print(json.dumps(result, indent=4))

# Run the test orchestrator when the script is executed
asyncio.run(test_orchestrator())
