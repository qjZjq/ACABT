def react(api, question, format = ""):
    pass

def cot(api, question, format = ""):
    msgs = [{"role": "user", "content": f"{question}\nLet's think step by step."}]
    print("Thinking...")
    think = api(msgs)
    msgs.append({"role": "assistant", "content": think})
    msgs.append({"role": "user", "content": f"{format}\nSo your answer is:"})
    print("Answering...")
    ans = api(msgs)
    return ans, think
    
def reflexion(api, question, iter, format = "", reasoning_method = "cot", verbose = False):
    info = []
    hint = ""
    for i in range(iter):
        if reasoning_method == "cot":
            A, reasoning = cot(api, hint + question, format)
        else:
            A, reasoning = react(api, hint + question, format)
            
        print("Reflecting...")
        R = api(f"""For a question:
{question}

You should examine the correctness of the following answer:
{reasoning}

Analyze it and after that give a reflection in brief how the answer can be improved (in 30 words) with the format of \"Reflect: <the reflection>\"""")
        hint += "Solution no.1: " + A + "\nReflection for an handed solution no.1: " + R.split("Reflect: ")[-1] + "\n"
        info += [(reasoning, A, R)]
        
        if verbose:
            print("COT\n" + reasoning)
            print("REFLECT\n" + R)
    return A, info

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
            model = "qwen2.5-7b-instruct",
            messages = msgs
        )
        return res.choices[0].message.content
    
    ans, info = reflexion(
        api,
        "Solve a \'Game of 24\': for 4 number 1,5,5,5, every time you remove two of them and replaced with one after applying +,-,* or /. Give a proccess of it so that you finally get only one number of 24.",
        5,
        reasoning_method = "cot",
        verbose = True,
    )
    
    print(ans)
    