def generate_to_refine(context):
    """
    Transition from `generate_plan` to `refine_plan`.
    - context: A dictionary containing the generated plan and other user data.
    """
    plan = context.get("generated_plan")
    if plan:
        return "refine_plan", {"message": f"Here is your initial plan:\n{plan}\nWould you like to refine it?"}
    else:
        return "generate_plan", {"message": "I couldn't generate the plan. Please check your inputs and try again."}
