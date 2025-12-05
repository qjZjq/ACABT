def gen_adversary(
    api,
    query : str,
    answer : str,
) -> str:
    return api(f"""For a question:
{query}

One answer is:
{answer}

Even if the final answer might be right, it could be vulnerable, such as logical fault, low efficiency, or other approaches. So you should assume it is not flawless and pick up at least one of its weak links. Give them in brief, with the format of:
weak link 1: ...
weak link 2: ...
...""")
    
def refine(
    api,
    query : str,
    prev : str,
    adversaries : str,
    num : int = 3,
) -> list[str]:
    return [api(
        f"""For a question:
{query}

One previous answer is:
{prev}

However a critic suspected that:
{adversaries}
(igore if it is a groundless accusation)

Based on the previous answer, correct only the suspicious part of it and print a new version of the answer:""",
    ) for _ in range(num)]