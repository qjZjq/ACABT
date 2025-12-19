def evaluate(
    api,
    query,
    answer_versions,
    critics,
    refines,
    mode : str = "critic_based",
) -> dict:
    evals = []
    
    for ans in refines:
        if mode == "llm_judge":
            res = api(
                f"For a question:\n{query}\n\nA solution is:\n{ans}\n\nIs it correct? Give a capital word \"YES\" or \"NO\"."
            ).find("YES") != -1
        elif mode == "critic_based":
            critic = critics
            if len(answer_versions) > 1:
                critic = answer_versions[-2]["ans"] + "\n" + critic
            res = api(
                f"For a question:\n{query}\n\nPrevious solutions meets following suspicions:\n{critic}\n\nA new solution is:\n{ans}\n\nIs there any suspicion unsettled in the new answer? Give a capital word \"YES\" or \"NO\"."
            ).find("NO") != -1
        evals.append(1 if res else 0)
    
    return evals