from enum import Enum, IntEnum
from dataclasses import dataclass
from typing import List, Optional
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download the sentiment analysis tool (only needed once)
nltk.download('vader_lexicon')

class TicketCategory(Enum):
    """
    Enum representing different categories of support tickets.
    """
    TECHNICAL = "technical"
    BILLING = "billing"
    FEATURE = "feature"
    ACCESS = "access"

class Priority(IntEnum):
    """
    Enum representing priority levels for tickets, supporting numeric comparisons.
    """
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

@dataclass
class TicketAnalysis:
    """
    Data structure representing the analysis result of a support ticket.

    Attributes:
        category (TicketCategory): The identified category of the ticket.
        priority (Priority): The assigned priority level.
        key_points (List[str]): Key points extracted from the ticket content.
        required_expertise (List[str]): List of required expertise for resolution.
        sentiment (float): Sentiment score of the ticket content (-1 to 1).
        urgency_indicators (List[str]): Words that indicate urgency in the ticket.
        business_impact (str): Level of business impact (Low, Medium, High).
        suggested_response_type (str): The type of response suggested (e.g., immediate).
        follow_up_required (bool): Whether a follow-up action is needed.
    """
    category: TicketCategory
    priority: Priority
    key_points: List[str]
    required_expertise: List[str]
    sentiment: float
    urgency_indicators: List[str]
    business_impact: str
    suggested_response_type: str
    follow_up_required: bool

class TicketAnalysisAgent:
    """
    AI-driven agent for analyzing support tickets.
    It categorizes tickets, assigns priority, detects urgency, sentiment,
    and determines if follow-ups are required.
    """

    def __init__(self):
        """
        Initializes the Ticket Analysis Agent with an NLTK Sentiment Analyzer.
        """
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    async def analyze_ticket(self, ticket_content: str, customer_info: Optional[dict] = None) -> TicketAnalysis:
        """
        Analyzes a support ticket to classify its category, determine priority,
        detect sentiment, urgency, and necessary expertise.

        Args:
            ticket_content (str): The text of the support ticket.
            customer_info (Optional[dict]): Additional customer information (role, name).

        Returns:
            TicketAnalysis: The structured analysis of the ticket.

        Example:
            analysis = await agent.analyze_ticket("I can't log in to my account. Please fix ASAP!", {"role": "Admin"})
        """

        # **Step 1: Identify Ticket Category**
        if any(word in ticket_content.lower() for word in ["access", "login", "403", "admin"]):
            category = TicketCategory.ACCESS
        elif any(word in ticket_content.lower() for word in ["billing", "invoice", "payment"]):
            category = TicketCategory.BILLING
        elif any(word in ticket_content.lower() for word in ["feature request", "enhancement"]):
            category = TicketCategory.FEATURE
        else:
            category = TicketCategory.TECHNICAL

        # **Step 2: Detect Sentiment Score**
        sentiment_score = self.sentiment_analyzer.polarity_scores(ticket_content)["compound"]

        # **Step 3: Detect Urgency Indicators**
        urgency_words = ["urgent", "asap", "immediately", "critical", "payroll", "important"]
        urgency_indicators = [word for word in urgency_words if word in ticket_content.lower()]

        # **Step 4: Determine Business Impact**
        business_impact = "Low"
        if "payroll" in ticket_content.lower():
            business_impact = "High"

        # **Step 5: Assign Priority**
        if "urgent" in urgency_indicators or business_impact == "High":
            priority = Priority.URGENT
        elif "important" in urgency_indicators:
            priority = Priority.HIGH
        elif category == TicketCategory.BILLING:
            priority = Priority.MEDIUM
        elif business_impact == "Medium":
            priority = Priority.MEDIUM
        elif sentiment_score < -0.5:  # ✅ Increase priority if sentiment is very negative
            priority = Priority.MEDIUM
        else:
            priority = Priority.LOW  # Default case

        # **Step 6: Identify Required Expertise**
        required_expertise = ["Support Specialist"]
        if category == TicketCategory.ACCESS:
            required_expertise.append("Security Expert")
        elif category == TicketCategory.BILLING:
            required_expertise.append("Billing Specialist")

        # **Step 7: Extract Key Points**
        key_points = [sentence.strip() for sentence in ticket_content.split("\n") if sentence.strip()]

        # **Step 8: Determine Suggested Response Type**
        suggested_response_type = "standard"
        if priority == Priority.URGENT:
            suggested_response_type = "immediate"

        # **Step 9: Determine if Follow-up is Required**
        follow_up_required = False
        follow_up_words = ["confirm", "verify", "clarify", "follow-up", "double-check"]
        if any(word in ticket_content.lower() for word in follow_up_words):
            follow_up_required = True

        return TicketAnalysis(
            category=category,
            priority=priority,
            key_points=key_points,
            required_expertise=required_expertise,
            sentiment=sentiment_score,
            urgency_indicators=urgency_indicators,
            business_impact=business_impact,
            suggested_response_type=suggested_response_type,
            follow_up_required=follow_up_required
        )
