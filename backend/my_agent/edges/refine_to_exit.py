def refine_to_exit(context):
    """
    Transition from `refine_plan` to an exit or completion state.
    - context: A dictionary containing the final user-approved plan.
    """
    approved_plan = context.get("approved_plan")
    if approved_plan:
        return "exit", {"message": "Your plan has been finalized. Thank you for using the plan maker!"}
    else:
        return "refine_plan", {"message": "Let me know if there’s anything else you’d like to change before finalizing."}
