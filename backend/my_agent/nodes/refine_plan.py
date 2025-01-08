from langgraph import Node

class RefinePlanNode(Node):
    def process(self, context):
        """
        Refine the plan based on user feedback.
        - context: A dictionary containing the current session data.
        """
        generated_plan = context.get("generated_plan")
        if not generated_plan:
            return {
                "message": "I couldn't find the generated plan. Please regenerate it before refining."
            }

        return {
            "message": (
                "What changes would you like to make to the plan?\n"
                "- Add/remove tasks?\n"
                "- Adjust deadlines or priorities?\n"
                "Please provide your feedback."
            )
        }
