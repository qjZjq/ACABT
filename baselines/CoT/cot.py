def cot(api, question, format = ""):
    msgs = [{"role": "user", "content": f"{question}\nLet's think step by step."}]
    print("Thinking...")
    think = api(msgs)
    msgs.append({"role": "assistant", "content": think})
    msgs.append({"role": "user", "content": f"{format}\nSo your answer is:"})
    print("Answering...")
    ans = api(msgs)
    return ans, {
        "think": think,
        "answer": ans,
    }

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
            messages = msgs
        )
        return res.choices[0].message.content
    
    ans, info = cot(
        api,
        "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?",
    )
    
    print(info["think"])
    print(ans)
    