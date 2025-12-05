def evaluate(
    api,
    query,
    answer_versions,
    adversaries,
    refines,
) -> dict:
    evals = {"adversary": 0, "answers": []}
    sus = [x[x.find(':')+1:] for x in adversaries.split("weak link")[1:]]
    for prev_adv in answer_versions[1::2]:
        for x in prev_adv["ans"].split("weak link")[1:]:
            sus.append(x[x.find(':') + 1:])
        for bro in prev_adv["bros"]:
            for x in bro.split("weak link")[1:]:
                sus.append(x[x.find(':') + 1:])
        
    
    for ans in refines:
        cnt = 0
        for s in sus:
            res = api(
                f"""For a question:
{query}

There is a solution:
{ans}

Check whether it matches the following suspicion:
{s}

Print \"YES\" if yes; or print \"NO\" if no."
"""
            )
            if res.find("YES") != -1:
                cnt += 1
        evals["answers"].append(cnt)
    
    return evals