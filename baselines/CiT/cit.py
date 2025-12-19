from openai import OpenAI

class Node:
    def __init__(self, conversation, parent):
        self.conversation = conversation
        self.parent = parent

class citTree:
    def __init__(self, policy_api, eval_api, verbose = False, **paras):
        self.eval = eval_api
        self.policy = policy_api
        self.nodes = []
        
        kbn = paras.get("Kbn", 4)
        method = paras.get("bn_method", "SC")
        if method == "DP":
            kbn = 1
        self.kbn = kbn
        self.method = method
        
        self.Rconf = paras.get("Rconf", 1)
        self.Rbn = paras.get("Rbn", 0.6)
        self.max_depth = paras["L"]
        self.k_final_verify = paras.get("K_vote", 5)
        
        self.verbose = verbose
    
    def IS_TERMINAL(self, s : Node):
        res = self.eval(s.conversation[:-1] + [{"role": "user", "content": "Is the question solved, or more steps are needed? Give a word in capital \"YES\" if you finish solving; or \"NO\" if not."}])
        return res.find("YES") != -1
    def BN_DP(self, s, a):
        pass
    def EQ(self, s : Node, a1, a2):
        res = self.eval(s.conversation[:-1] + [{"role": "user", "content": f"For the next step, I think of two ways:\n(1) {a1}\n(2) {a2}\n\nAre they almost the same? Give a word in capital \"YES\" or \"NO\"."}])
        return res.find("YES") != -1
    def BN_SC(self, s, A):
        prs = [(i,j) for j in range(1, self.kbn) for i in range(j) if self.EQ(s, A[i], A[j])]
        clusters = [set((i,)) for i in range(self.kbn)]
        for x, y in prs:
            u = clusters[x] | clusters[y]
            for e in u:
                clusters[e] = u
        mx = max(len(c) for c in clusters)
        
        ans = []
        for i in range(self.kbn):
            if i == min(clusters[i]):
                ans.append([len(clusters[i]), A[i]])
        ans.sort(key = lambda x: x[0], reverse = True)
        return ans[0][0] / len(A), [x[1] for x in ans]
    
    def gen(self, s : Node, K):
        return [self.policy(s.conversation) for _ in range(K)]
    def trans(self, node, clusters):
        nex = []
        for a in clusters:
            nex.append(len(self.nodes))
            self.nodes.append(Node(
                self.nodes[node].conversation + [
                    {"role":"assistant", "content":a},
                    {"role":"user", "content":"Give a brief process of the next step."},
                ],
                node,
            ))
        return nex, -1
    def CiT_bfs(self, query, max_ans = 10):
        self.nodes = [Node([
            {"role": "system", "content": f"{query}\n To solve this question, the user will ask you step by step."},
            {"role": "user", "content": "Give a brief process of the first step."}
        ], -1)]
        frontier = [[0]]
        ans = []
        
        for depth in range(self.max_depth + 1):
            if self.verbose: print("Layer", depth, "-- total", len(frontier[depth]))
            
            frontier.append([])
            for node in frontier[depth]:
                if (depth > 0) and self.IS_TERMINAL(self.nodes[node]):
                    ans.append(self.nodes[node].conversation)
                    continue
                if depth == self.max_depth:
                    continue
                if len(ans) >= max_ans:
                    break
                    
                A = self.gen(self.nodes[node], self.kbn)
                if self.method == "DP":
                    ev, clusters = self.BN_DP(self.nodes[node], A[0])
                else:
                    ev, clusters = self.BN_SC(self.nodes[node], A)
                    
                if ev > self.Rbn:
                    clusters = clusters[:1]
                
                nex, r_conf = self.trans(node, clusters)
                frontier[depth + 1] += nex
                
        votes = self.fast_score(query, ans)
        if ans:
            result = max(zip(votes, ans), key = lambda x: x[0])[1]
        else:
            result = None
        return result, {"tree":self.nodes, "candidates": ans, "votes": votes}
    
    def fast_score(self, query, answer):
        if not answer:
            return []
        if isinstance(answer[0], dict):
            solution = "\n\n".join([x["content"] for x in answer[2::2]])
            prompt = f"For a problem:\n{query}\n\nA solution is:\n{solution}\n\nDo you think it is correct?Give a capital word \"YES\" or \"NO\"."
            return sum(self.eval(prompt).find("YES") != -1 for _ in range(self.k_final_verify))
        else:
            return [self.fast_score(query, a) for a in answer]
        
    
    
if __name__ == "__main__":
    client = OpenAI(
        api_key = "sk-89d43b4e34fa487a92311a78c8a393ab",
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    
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
    
    tree = citTree(policy_api, eval_api, verbose = True, L = 7)
    result, info = tree.CiT_bfs("Solve a \'Game of 24\': for 4 number 1,5,5,5, every time you remove two of them and replaced with one after applying +,-,* or /. Give a proccess of it so that you finally get only one number of 24.")
    print("SIZE", len(info["tree"]))
    for x in result[2::2]:
        print("#"*100)
        print(x["content"])
        print()
    