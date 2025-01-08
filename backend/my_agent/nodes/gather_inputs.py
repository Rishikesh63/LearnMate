from langgraph import Node

class GatherInputsNode(Node):
    def process(self, context):
        """
        Gather detailed inputs for the plan.
        - context: A dictionary containing the current session data.
        """
        if "tasks" not in context:
            context["tasks"] = []
        if "deadlines" not in context:
            context["deadlines"] = []
        
        return {
            "message": (
                "Please provide the details of your plan:\n"
                "- What tasks or goals need to be accomplished?\n"
                "- Are there any specific deadlines or priorities?"
            )
        }
