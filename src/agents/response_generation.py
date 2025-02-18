from typing import Dict, Any

class ResponseAgent:
    """
    The ResponseAgent generates an AI-powered response based on the ticket analysis.
    It formats responses using predefined templates and determines if escalation is required.
    """

    async def generate_response(self, ticket_analysis, response_templates: Dict[str, str], context: Dict[str, Any]):
        """
        Generates a response based on the ticket analysis, using predefined templates.

        Args:
            ticket_analysis: The result of the ticket analysis, containing category, priority, etc.
            response_templates (Dict[str, str]): A dictionary containing predefined response templates.
            context (Dict[str, Any]): Additional customer information (e.g., customer name).

        Returns:
            dict: A dictionary containing the generated response details:
                - response_text (str): The formatted response message.
                - confidence_score (float): The confidence level of the response (default 0.9).
                - requires_approval (bool): Whether the response requires approval (True for urgent priority).
                - suggested_actions (list): Recommended actions, such as escalation.

        Example:
            response_templates = {
                "access": "Hello {name}, we are fixing your {feature}. Priority: {priority_level}. ETA: {eta}."
            }
            context = {"customer_name": "Alice"}
            result = await response_agent.generate_response(ticket_analysis, response_templates, context)
        """
        category = ticket_analysis.category.value
        template = response_templates.get(category, "Hello {name}, we are working on your request.")

        response_text = template.format(
            name=context.get("customer_name", "Customer"),
            feature="dashboard" if category == "access" else "service",
            priority_level=ticket_analysis.priority.name,
            eta="1 hour" if ticket_analysis.priority == 4 else "24 hours",
        )

        return {
            "response_text": response_text,
            "confidence_score": 0.9,
            "requires_approval": ticket_analysis.priority == 4,
            "suggested_actions": ["Escalate to senior team"] if ticket_analysis.priority == 4 else []
        }
