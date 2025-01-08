def type_to_inputs(context):
    """
    Transition from `ask_plan_type` to `gather_inputs`.
    - context: A dictionary containing user inputs and the current state.
    """
    plan_type = context.get("plan_type")
    if plan_type:
        return "gather_inputs", {"message": f"Let's gather details for your {plan_type}."}
    else:
        return "ask_plan_type", {"message": "Please specify the type of plan you'd like to create."}
