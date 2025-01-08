def refine_to_generate(context):
    """
    Transition from `refine_plan` back to `generate_plan` for iterative refinement.
    - context: A dictionary containing feedback and updated inputs.
    """
    feedback = context.get("refinement_feedback")
    if feedback:
        return "generate_plan", {"message": "Regenerating the plan based on your feedback."}
    else:
        return "refine_plan", {"message": "Please provide specific feedback to refine your plan."}
