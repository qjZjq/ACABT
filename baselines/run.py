from .CoT.cot import cot
from .reflexion.reflexion import reflexion

def baselines(api, method, query, ans_format = "", **kwargs):
    if method == "CoT":
        return cot(api, query, ans_format)
    if method == "reflexion":
        return reflexion(api, query, kwargs.get("iter", 5), ans_format)