from copilotkit import PlanGenerator

class GeneratePlanNode(Node):
    def process(self, context):
        """
        Generate the plan using the provided inputs.
        - context: A dictionary containing the current session data.
        """
        tasks = context.get("tasks", [])
        deadlines = context.get("deadlines", [])
        priorities = context.get("priorities", {})

        if not tasks:
            return {
                "message": "I couldn't find any tasks to generate a plan. Please go back and provide more details."
            }

        # Generate the plan using CopilotKit or custom logic
        generated_plan = PlanGenerator.create_plan(tasks, deadlines, priorities)
        context["generated_plan"] = generated_plan

        return {
            "message": f"Here is your plan:\n{generated_plan}\nWould you like to refine it?"
        }
