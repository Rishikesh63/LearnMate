def inputs_to_generate(context):
    """
    Transition from `gather_inputs` to `generate_plan`.
    - context: A dictionary containing user inputs like tasks, deadlines, and priorities.
    """
    tasks = context.get("tasks", [])
    if tasks:
        return "generate_plan", {"message": "Generating your plan based on the provided inputs."}
    else:
        return "gather_inputs", {"message": "I need at least one task or goal to proceed. Please provide more details."}
