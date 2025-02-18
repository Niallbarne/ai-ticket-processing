import asyncio
from src.agents.ticket_analysis import TicketAnalysisAgent, Priority, TicketCategory

async def test_ticket_analysis():
    """
    Tests the TicketAnalysisAgent by analyzing different ticket scenarios.
    
    The test cases cover:
    - High-priority access issues.
    - Negative sentiment detection.
    - Billing inquiries.
    - Follow-up requirement detection.

    The function ensures that tickets are correctly categorized, prioritized, and analyzed for sentiment and urgency.
    """

    agent = TicketAnalysisAgent()

    # ✅ Test Case 1: High Priority Access Issue
    print("\n🔹 Running Test Case 1: High Priority Access Issue")
    ticket1 = {
        "content": "I can't access my account. Urgent fix needed. I need to process payroll today.",
        "customer_info": {"role": "Finance Director"}
    }
    result1 = await agent.analyze_ticket(ticket1["content"], ticket1["customer_info"])
    print("🔍 Debug Info:", vars(result1))

    assert result1.priority == Priority.URGENT, f"❌ Expected priority URGENT, but got {result1.priority}"
    assert result1.category == TicketCategory.ACCESS, f"❌ Expected category 'ACCESS', got {result1.category}"
    assert "urgent" in result1.urgency_indicators, f"❌ Missing 'urgent' in urgency indicators: {result1.urgency_indicators}"
    print("✅ Test Case 1 Passed!")

    # ✅ Test Case 2: Negative Sentiment Analysis
    print("\n🔹 Running Test Case 2: Negative Sentiment Analysis")
    ticket2 = {
        "content": "Your system is absolutely terrible! I am very disappointed.",
        "customer_info": {"role": "Customer"}
    }
    result2 = await agent.analyze_ticket(ticket2["content"], ticket2["customer_info"])
    print("🔍 Debug Info:", vars(result2))

    assert result2.sentiment < -0.5, f"❌ Expected sentiment < -0.5, but got {result2.sentiment}"
    assert int(result2.priority) >= int(Priority.MEDIUM), f"❌ Expected priority at least MEDIUM, but got {result2.priority}"
    print("✅ Test Case 2 Passed!")

    # ✅ Test Case 3: Billing Inquiry
    print("\n🔹 Running Test Case 3: Billing Inquiry")
    ticket3 = {
        "content": "Can you explain how the billing cycle works?",
        "customer_info": {"role": "Billing Admin"}
    }
    result3 = await agent.analyze_ticket(ticket3["content"], ticket3["customer_info"])
    print("🔍 Debug Info:", vars(result3))

    assert result3.category == TicketCategory.BILLING, f"❌ Expected category 'BILLING', got {result3.category}"
    assert result3.priority == Priority.MEDIUM, f"❌ Expected priority MEDIUM, got {result3.priority}"
    print("✅ Test Case 3 Passed!")

    # ✅ Test Case 4: Follow-up Required
    print("\n🔹 Running Test Case 4: Follow-up Required")
    ticket4 = {
        "content": "Please confirm the details before I proceed.",
        "customer_info": {"role": "User"}
    }
    result4 = await agent.analyze_ticket(ticket4["content"], ticket4["customer_info"])
    print("🔍 Debug Info:", vars(result4))

    assert result4.follow_up_required is True, f"❌ Expected follow_up_required to be True, got {result4.follow_up_required}"
    print("✅ Test Case 4 Passed!")

# Run the test cases
asyncio.run(test_ticket_analysis())
