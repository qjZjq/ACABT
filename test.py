from openai import OpenAI

client = OpenAI(
    api_key = "sk-89d43b4e34fa487a92311a78c8a393ab",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    # base_url = "https://api.chatanywhere.tech/v1",
    # api_key = "sk-RDAwatfI7Vb9M5RSvKHPuq7g73KiFk6gVyQlOYJAK6eRF9Zz",
)
def api(msgs):
    if isinstance(msgs, str):
        msgs = [{"role": "user", "content": msgs}]
    res = client.chat.completions.create(
        # model = "gpt-4",
        model = "qwen3-max",
        # model = "deepseek-v3",
        messages = msgs,
        max_tokens = 1000,
    )
    answer = res.choices[0].message.content
    if res.choices[0].finish_reason != "stop":
        answer += "<truncated due to length limit>"
    return answer


from baselines.run import baselines
from AnsTree.main_loop import run
from getdata import read

import re
import json

data, ans_format = read("AIME25")

if False:
    CoTs = []
    cnt = 0
    for i, x in enumerate(data):
        print("TEST",i)
        res, info = baselines(api, "CiT", x["problem"], ans_format, tree_search_method = "tot", client = client)
        CoTs.append(info)
        try:
            ans = int(re.findall(r"\d+", res)[0])
            if ans != x["answer"]:
                print("WA:", res, "ANS:", x["answer"])
            else:
                print("CORRECT")
                cnt += 1
        except:
            print("WA:", res, "ANS:", x["answer"])
    print(cnt)
    
    with open("cit_log.json", "w") as f:
        json.dump(CoTs, f)
else:
    trees = []
    cnt = 0
    for i, x in enumerate(data):
        print("TEST",i)
        res, info = run(api, x["problem"], iter = 5, answer_format = ans_format, mode = "tree")
        info["final_ans"] = res
        trees.append(info)
        try:
            ans = int(re.findall(r"\d+", res)[0])
            if ans == x["answer"]:
                print("CORRECT")
                cnt += 1
            else:
                print("WA:", res, "ANS:", x["answer"])
        except:
            print("WA:", res, "ANS:", x["answer"])
    print(cnt)
    
    with open("ACtree_log.json", "w") as f:
        json.dump(trees, f)