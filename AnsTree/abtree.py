import math
# UCB
def calc_ucb(v, N, n, c):
    return v + c * math.sqrt(2.0 * math.log(N) / (n))

# Alpha-Beta Tree
class AlphaBetaTree:
    def __init__(
        self,
        max_childs : int = 3,
        ucb_coeff : float = 0.5,
    ) -> None:
        self.max_childs = max_childs
        self.id = 0
        self.ans = []
        self.parent = []
        self.child = []
        self.v = []
        self.reward = []
        self.odd_depth = []
        
        self.c = ucb_coeff
        self.cnt = []
        
    def update(
        self,
        x : int,
    ) -> None:
        if x == -1: return
        
        if self.child[x]:
            if self.odd_depth:
                m = min(self.v[c] for c in self.child[x])
            else:
                m = max(self.v[c] for c in self.child[x])
                m = max(m, self.reward[x])
        else:
            m = self.reward[x]
        
        self.v[x] = m
        self.update(self.parent[x])
        
    def addnode(
        self,
        parent : int,
        ans : str,
        reward : float,
    ) -> int:
        self.ans.append(ans)
        self.parent.append(parent)
        self.v.append(0)
        self.reward.append(reward)
        self.child.append([])
        if parent != -1:
            self.odd_depth.append(not self.odd_depth[parent])
            self.child[parent].append(self.id)
            self.cnt[parent] += 1
        else:
            self.odd_depth.append(False)
            
        self.cnt.append(1)
        self.id += 1
        
        self.update(self.id - 1)
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
        res = min(selected_from, key = lambda x: self.reward[x])
        return self.ans[res]
        