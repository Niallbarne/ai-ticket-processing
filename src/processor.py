import asyncio
import json
from src.agents.ticket_analysis import TicketAnalysisAgent
from src.agents.response_generation import ResponseAgent

class TicketProcessor:
    """
    Orchestrates the processing of support tickets by combining the analysis and response generation agents.

    This class uses the TicketAnalysisAgent to analyze a ticket and then the ResponseAgent
    to generate an appropriate response based on the analysis.
    """

    def __init__(self):
        """
        Initializes the TicketProcessor with instances of TicketAnalysisAgent and ResponseAgent.
        """
        self.analysis_agent = TicketAnalysisAgent()
        self.response_agent = ResponseAgent()

    async def process_ticket(self, ticket):
        """
        Processes a single support ticket by analyzing its content and generating a response.

        Steps:
            1. Analyze the ticket using the TicketAnalysisAgent.
            2. Load response templates from the JSON file.
            3. Generate a response using the ResponseAgent.
            4. Print the analysis results and the generated response.

        Args:
            ticket (dict): A dictionary containing:
                - "content": The text of the support ticket.
                - "customer_info": A dictionary with customer information (e.g., customer_name, role).
        """
        # Step 1: Analyze the ticket
        analysis = await self.analysis_agent.analyze_ticket(ticket["content"], ticket["customer_info"])

        # Step 2: Load response templates
        with open("data/response_templates.json", "r") as file:
            response_templates = json.load(file)

        # Step 3: Generate response
        response = await self.response_agent.generate_response(analysis, response_templates, ticket["customer_info"])

        # Print results
        print("\n===== Ticket Analysis Result =====")
        print(f"Category: {analysis.category.value}")
        print(f"Priority: {analysis.priority.name}")
        print(f"Sentiment Score: {analysis.sentiment}")
        print(f"Urgency Indicators: {analysis.urgency_indicators}")
        print(f"Follow-up Required: {analysis.follow_up_required}")

        print("\n===== Generated Response =====")
        print(response["response_text"])
        print(f"Requires Approval: {response['requires_approval']}")
        print(f"Suggested Actions: {response['suggested_actions']}")

async def main():
    """
    Main function to run the ticket processing workflow.

    It creates a sample ticket, instantiates a TicketProcessor, and processes the ticket.
    """
    # Sample Ticket
    ticket = {
        "content": "I can't access my dashboard. I keep getting a 403 error. This is urgent!",
        "customer_info": {"customer_name": "Alice", "role": "Finance Director"}
    }

    processor = TicketProcessor()
    await processor.process_ticket(ticket)

# Run the main function when the script is executed directly
asyncio.run(main())
