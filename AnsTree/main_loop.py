from .expand import gen_critic, refine
from .abtree import AlphaBetaTree
from .eval import evaluate

def run(
    api,
    query : str,
    answer_format : str = "",
    iter : int = 16,
    max_refine : int = 3,
    mode : str = "tree",
):
    if mode == "tree":
        tree = AlphaBetaTree(max_childs = max_refine)
        ans0 = api(query)
        tree.set_root(ans0, 0.0)
        
        for i in range(iter):
            ans, x = tree.get_max_ucb()
            path_to_root = tree.get_path_to_root(x)
            
            adv = gen_critic(api, query, ans)
            new_ans = refine(api, query, ans, adv, max_refine)
            evals = evaluate(api, query, path_to_root, adv, new_ans)
            
            node_critic = tree.addnode(x, adv, 0)
            for idx in range(max_refine):
                tree.addnode(node_critic, new_ans[idx], evals[idx])
            tree.update(node_critic)
                
        ans = tree.get_max_rw()
        if answer_format:
            msgs = [{"role": "user", "content": f"{query}"}]
            msgs.append({"role": "assistant", "content": ans})
            msgs.append({"role": "user", "content": f"{answer_format}\nSo your answer is:"})
            return api(msgs), tree.to_dict()
        else:
            return ans, tree.to_dict()
        
    elif mode == "chain":
        traj = []
        ans = api(query)
        for i in range(iter):
            print(f"ITER {i}", end = " ", flush = True)
            adv = gen_critic(api, query, ans)
            traj.append((ans, adv))
            ans = refine(api, query, ans, adv, 1)[0]
        traj.append((ans, None))
        print("SAMPLED.")
        
        if answer_format:
            msgs = [{"role": "user", "content": f"{query}"}]
            msgs.append({"role": "assistant", "content": ans})
            msgs.append({"role": "user", "content": f"{answer_format}\nSo your answer is:"})
            ans = api(msgs)
        return ans, traj
            
    