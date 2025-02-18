import asyncio
import json
from src.agents.response_generation import ResponseAgent
from src.agents.ticket_analysis import TicketAnalysis, TicketCategory, Priority

async def test_response_generation():
    """
    Tests the ResponseAgent by generating responses for different ticket scenarios.
    
    The test cases cover:
    - Urgent access issues that require escalation.
    - Normal billing inquiries that do not require escalation.
    
    The function loads response templates from a JSON file and ensures the ResponseAgent
    produces correct, structured responses.
    """

    agent = ResponseAgent()

    # ✅ Load Response Templates
    with open("data/response_templates.json", "r") as file:
        response_templates = json.load(file)

    # ✅ Test Case 1: Urgent Access Issue
    print("\n🔹 Running Test Case 1: Urgent Access Issue")
    ticket_analysis1 = TicketAnalysis(
        category=TicketCategory.ACCESS,
        priority=Priority.URGENT,
        key_points=["User unable to access dashboard"],
        required_expertise=["Support"],
        sentiment=-0.7,
        urgency_indicators=["urgent"],
        business_impact="High",
        suggested_response_type="immediate",
        follow_up_required=False
    )
    context1 = {"customer_name": "Alice"}
    result1 = await agent.generate_response(ticket_analysis1, response_templates, context1)

    print("🔍 Debug Info:", result1)
    assert "fixing your dashboard" in result1["response_text"], "❌ Incorrect response text"
    assert result1["requires_approval"] is True, "❌ Expected requires_approval to be True"
    assert "Escalate to senior team" in result1["suggested_actions"], "❌ Expected escalation action"
    print("✅ Test Case 1 Passed!")

    # ✅ Test Case 2: Normal Billing Inquiry
    print("\n🔹 Running Test Case 2: Billing Inquiry")
    ticket_analysis2 = TicketAnalysis(
        category=TicketCategory.BILLING,
        priority=Priority.MEDIUM,
        key_points=["Customer asking about billing cycle"],
        required_expertise=["Billing Specialist"],
        sentiment=0.0,
        urgency_indicators=[],
        business_impact="Low",
        suggested_response_type="standard",
        follow_up_required=True
    )
    context2 = {"customer_name": "Bob"}
    result2 = await agent.generate_response(ticket_analysis2, response_templates, context2)

    print("🔍 Debug Info:", result2)
    assert "billing inquiry" in result2["response_text"], "❌ Incorrect response text"
    assert result2["requires_approval"] is False, "❌ Expected requires_approval to be False"
    print("✅ Test Case 2 Passed!")

# Run the test cases
asyncio.run(test_response_generation())
