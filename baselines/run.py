from .CoT.cot import cot
from .reflexion.reflexion import reflexion
from .CiT.cit import citTree

def baselines(api, method, query, ans_format = "", **kwargs):
    if method == "CoT":
        return cot(api, query, ans_format)
    if method == "reflexion":
        return reflexion(api, query, kwargs.get("iter", 5), ans_format)
    if method == "CiT":
        client = kwargs["client"]
        def policy_api(msgs):
            if isinstance(msgs, str):
                msgs = [{"role": "user", "content": msgs}]
                
            res = client.chat.completions.create(
                model = "qwen3-max",
                messages = msgs,
                max_tokens = 500,
                temperature = 1.5,
            )
            return res.choices[0].message.content
        def eval_api(msgs):
            if isinstance(msgs, str):
                msgs = [{"role": "user", "content": msgs}]
                
            res = client.chat.completions.create(
                model = "qwen3-max",
                messages = msgs,
                max_tokens = 50,
            )
            return res.choices[0].message.content
        
        TS = kwargs.get("tree_search_method", "tot")
        if TS == "tot":
            tree = citTree(policy_api, eval_api, L=7)
            ans, info = tree.CiT_bfs(query)
            if ans:
                res = api(ans[:-1] + [{"role":"user", "content": f"{ans_format}\nSo give the final answer:"}])
                return res, info
            else:
                return None, info