import math
# UCB
def calc_ucb(v, N, n, c):
    return v + c * math.sqrt(2.0 * math.log(N) / (n))

# Alpha-Beta Tree
class AlphaBetaTree:
    def __init__(
        self,
        max_childs : int = 3,
        ucb_coeff : float = 0.3,
        gamma : float = 0.9,
    ) -> None:
        self.max_childs = max_childs
        self.id = 0
        self.ans = []
        self.parent = []
        self.child = []
        self.v = []
        self.reward = []
        self.score = []
        self.odd_depth = []
        
        self.c = ucb_coeff
        self.gamma = gamma
        self.cnt = []
        
    def update(
        self,
        x : int,
    ) -> None:
        if x == -1:
            return
        
        if self.odd_depth:
            self.v[x] = 0.5 * (min(self.v[c] for c in self.child[x]) + sum(self.v[c] for c in self.child[x]) / len(self.child[x]))
        else:
            self.v[x] = 0.5 * (max(self.v[c] for c in self.child[x]) + sum(self.v[c] for c in self.child[x]) / len(self.child[x]))
            
        self.update(self.parent[x])
        
    def addnode(
        self,
        parent : int,
        ans : str,
        reward : float,
    ) -> int:
        self.ans.append(ans)
        self.parent.append(parent)
        self.reward.append(reward)
        self.child.append([])
        if parent != -1:
            self.odd_depth.append(not self.odd_depth[parent])
            self.score.append(self.score[parent] * self.gamma + reward)
            self.child[parent].append(self.id)
            self.cnt[parent] += 1
        else:
            self.odd_depth.append(False)
            self.score.append(reward)
        self.v.append(self.score[-1])
            
        self.cnt.append(1)
        self.id += 1
        
        return self.id - 1
        
    def set_root(
        self,
        ans0 : str,
        reward : float,
    ) -> None:
        self.root = self.addnode(-1, ans0, reward)
        
    def get_max_ucb(
        self,
    ) -> tuple[str, int]:
        selected_from = [x for x in range(self.id) if (not self.odd_depth[x]) and (len(self.child[x]) < self.max_childs)]
        res = min(selected_from, key = lambda x: calc_ucb(self.v[x], self.id + 1, self.cnt[x], self.c))
        return self.ans[res], res
    
    def get_path_to_root(
        self,
        x,
    ):
        parent = self.parent[x]
        if parent == -1:
            return [{"ans": self.ans[x]}]
        else:
            prev = self.get_path_to_root(parent)
            return prev + [{"ans": self.ans[x], "bros": [self.ans[bro] for bro in self.child[parent] if bro != x]}]
        
    def get_max_rw(
        self,
    ) -> str:
        selected_from = [x for x in range(self.id) if not self.odd_depth[x]]
        res = min(selected_from, key = lambda x: self.score[x])
        return self.ans[res]
        
    def to_dict(self):
        return {
            "parent": self.parent,
            "child": self.child,
            "ans": self.ans,
            "reward": self.reward,
            "score": self.score,
            "v": self.v,
            "configs": {
                "max_childs": self.max_childs,
                "gamma": self.gamma,
                "c": self.c,
            },
        }