
class AskPlanTypeNode(Node):
    def process(self, context):
        """
        Ask the user about the type of plan they want to create.
        - context: A dictionary containing the current session data.
        """
        context["plan_type"] = None  # Initialize the plan type if not already set
        return {
            "message": "What type of plan would you like to create? (e.g., daily schedule, project roadmap, travel itinerary)"
        }

