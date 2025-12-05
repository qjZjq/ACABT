from .expand import gen_adversary, refine
from .abtree import AlphaBetaTree
from .eval import evaluate

def run(
    api,
    query : str,
    answer_format : str = "",
    iter : int = 16,
    max_refine : int = 3,
):
    tree = AlphaBetaTree(max_childs = max_refine)
    ans0 = api(query)
    tree.set_root(ans0, 0.0)
    
    for i in range(iter):
        ans, x = tree.get_max_ucb()
        path_to_root = tree.get_path_to_root(x)
        
        adv = gen_adversary(api, query, ans)
        new_ans = refine(api, query, ans, adv, max_refine)
        evals = evaluate(api, query, path_to_root, adv, new_ans)
        
        node_adv = tree.addnode(x, adv, evals["adversary"])
        print(evals["answers"])
        for idx in range(max_refine):
            tree.addnode(node_adv, new_ans[idx], evals["answers"][idx])
            
    ans = tree.get_max_rw()
    if answer_format:
        return api(query + "\n\nAn answer is:\n" + ans + "\n\nSummarize it into the following format:\n" + answer_format), ans
    else:
        return ans, ans
            
    