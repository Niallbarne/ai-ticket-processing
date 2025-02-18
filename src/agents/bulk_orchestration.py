import asyncio
import json
from src.agents.orchestrator import Orchestrator
from enum import Enum  

class BulkOrchestrator:
    """
    Handles bulk processing of multiple support tickets from a JSON file.
    Uses the Orchestrator to process each ticket and saves responses to an output file.
    """

    def __init__(self):
        """
        Initializes the BulkOrchestrator by creating an instance of Orchestrator.
        """
        self.orchestrator = Orchestrator()

    async def process_tickets(self, input_file: str, output_file: str):
        """
        Reads multiple tickets from a JSON file, processes them using the Orchestrator,
        and saves the processed results to another JSON file.

        Args:
            input_file (str): Path to the input JSON file containing support tickets.
            output_file (str): Path to the output JSON file to save processed ticket responses.

        Example:
            bulk_orchestrator.process_tickets("data/sample_tickets.json", "data/processed_tickets.json")
        """
        with open(input_file, "r") as file:
            tickets = json.load(file)

        processed_tickets = []
        for ticket in tickets:
            print(f"\n🔹 Processing Ticket: {ticket['content']}")
            result = await self.orchestrator.process_ticket(
                ticket["content"], ticket["customer_info"]
            )
            processed_tickets.append(result)

        # ✅ Fix: Serialize objects before saving
        with open(output_file, "w") as file:
            json.dump(processed_tickets, file, indent=4, default=self.serialize)

        print(f"\n✅ Bulk Processing Complete! Results saved to {output_file}")

    @staticmethod
    def serialize(obj):
        """
        Serializes objects to a JSON-compatible format.

        Args:
            obj: The object to serialize (can be an Enum, class instance, or list).

        Returns:
            A JSON-serializable representation of the object.

        Example:
            BulkOrchestrator.serialize(Priority.URGENT) -> "URGENT"
        """
        if isinstance(obj, Enum):  # ✅ Convert Enums to their string value
            return obj.value
        elif hasattr(obj, "__dict__"):  # ✅ Convert objects to dictionaries
            return {k: BulkOrchestrator.serialize(v) for k, v in obj.__dict__.items()}
        elif isinstance(obj, list):  # ✅ Convert lists recursively
            return [BulkOrchestrator.serialize(item) for item in obj]
        return obj  # ✅ Return normal values as-is

# ✅ Run bulk processing if executed directly
if __name__ == "__main__":
    async def run_bulk_processing():
        """
        Runs bulk processing on sample tickets.
        Reads tickets from 'data/sample_tickets.json' and saves results to 'data/processed_tickets.json'.
        """
        bulk_orchestrator = BulkOrchestrator()
        await bulk_orchestrator.process_tickets(
            "data/sample_tickets.json", "data/processed_tickets.json"
        )

    asyncio.run(run_bulk_processing())
