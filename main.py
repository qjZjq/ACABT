from AnsTree.main_loop import run
from baselines.run import baselines

if __name__ == "__main__":
    from openai import  OpenAI
    client = OpenAI(
        api_key = "sk-89d43b4e34fa487a92311a78c8a393ab",
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    def api(msgs):
        if isinstance(msgs, str):
            msgs = [{"role": "user", "content": msgs}]
        res = client.chat.completions.create(
            model = "qwen3-max",
            messages = msgs,
            max_tokens = 800,
        )
        return res.choices[0].message.content
    
    ans, info = baselines(
        api,
        "CoT",
        """For $\{1, 2, 3, \ldots, n\}$ and each of its non-empty subsets a unique alternating sum is defined as follows. Arrange the numbers in the subset in decreasing order and then, beginning with the largest, alternately add and subtract successive numbers. For example, the alternating sum for $\{1, 2, 3, 6,9\}$ is $9-6+3-2+1=5$ and for $\{5\}$ it is simply $5$. Find the sum of all such alternating sums for $n=7$.""",
    )
    
    print(ans)
    print(info["think"])
    